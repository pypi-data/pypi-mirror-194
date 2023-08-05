"""S3 storage module."""
import re
import typing as t

import boto3
import boto3.s3.transfer
import botocore.client
import botocore.config
import botocore.exceptions as s3_errors
from fw_utils import AnyFile, Filters

from .. import errors
from ..config import S3Config
from ..fileinfo import FileInfo
from ..filters import StorageFilter
from ..storage import AnyPath, CloudStorage

__all__ = ["S3Storage"]

# TODO consider making these configurable
CHUNKSIZE = 8 << 20
TRANSFER_CONFIG = boto3.s3.transfer.TransferConfig(
    multipart_chunksize=CHUNKSIZE, io_chunksize=CHUNKSIZE
)


ERRMAP = {
    s3_errors.ClientError: errors.StorageError,
    s3_errors.BotoCoreError: errors.StorageError,
}


def convert_s3_error(exc: Exception) -> t.Type[errors.StorageError]:
    """Return specific S3 errors mapped to StorageError types."""
    if isinstance(exc, s3_errors.ClientError):
        status_code = exc.response["ResponseMetadata"]["HTTPStatusCode"]
        if status_code == 403:
            return errors.PermError
        if status_code == 404:
            return errors.FileNotFound
    return errors.StorageError


errmap = errors.ErrorMapper(ERRMAP, convert_s3_error)  # type: ignore


class S3Storage(CloudStorage):
    """AWS S3 Storage class."""

    def __init__(
        self,
        config: S3Config,
        **kwargs,
    ):
        """AWS S3 Storage class for working with blobs in S3 buckets.

        Args:
            config: S3Config
        """
        self.config = config

        # https://boto3.amazonaws.com/v1/documentation/api/latest/guide/credentials.html
        client_config = botocore.config.Config(
            signature_version="s3v4",
            retries={"max_attempts": 3},
        )
        secret = None
        if self.config.secret_access_key:
            secret = self.config.secret_access_key.get_secret_value()
        session = boto3.session.Session(
            aws_access_key_id=self.config.access_key_id,
            aws_secret_access_key=secret,
        )
        self.client = session.client("s3", config=client_config)

        super().__init__(**kwargs)

    def abspath(self, path: AnyPath) -> str:
        """Return path string relative to the storage URL, including the perfix."""
        return f"{self.config.prefix}/{self.relpath(path)}".lstrip("/")

    def fullpath(self, path: AnyPath) -> str:
        """Return path string including the storage URL and prefix."""
        return f"s3://{self.config.bucket}/{self.abspath(path)}".rstrip("/")

    @errmap
    def ls(
        self,
        path: AnyPath = "",
        *,
        include: Filters = None,
        exclude: Filters = None,
        **_,
    ) -> t.Iterator[FileInfo]:
        """Yield each item under prefix matching the include/exclude filters."""
        # https://docs.aws.amazon.com/AmazonS3/latest/userguide/using-folders.html
        # https://docs.aws.amazon.com/AmazonS3/latest/API/API_Object.html
        filt = StorageFilter(include=include, exclude=exclude)
        paginator = self.client.get_paginator("list_objects_v2")
        prefix = f"{self.config.prefix}/{path}".strip("/")
        if prefix:
            prefix += "/"
        pages = paginator.paginate(Bucket=self.config.bucket, Prefix=prefix)
        for page in pages:
            for meta in page.get("Contents", []):
                filepath: str = meta["Key"]
                relpath = re.sub(rf"^{self.config.prefix}", "", filepath).lstrip("/")
                info = FileInfo(
                    path=relpath,
                    size=meta["Size"],
                    hash=meta["ETag"][1:-1],
                    created=meta["LastModified"].timestamp(),  # TODO consider None
                    modified=meta["LastModified"].timestamp(),
                )
                # skip s3 "folders" - path is empty if the prefix itself is a "folder"
                if not relpath or relpath.endswith("/") and info.size == 0:
                    continue  # pragma: no cover
                if filt.match(info):
                    yield info

    @errmap
    def stat(self, path: AnyPath) -> FileInfo:
        """Return FileInfo for a single file."""
        meta = self.client.head_object(
            Bucket=self.config.bucket, Key=self.abspath(path)
        )
        return FileInfo(
            path=str(path),
            size=meta["ContentLength"],
            hash=meta["ETag"][1:-1],
            created=meta["LastModified"].timestamp(),  # TODO consider None
            modified=meta["LastModified"].timestamp(),
        )

    @errmap
    def download_file(self, path: str, dst: t.IO[bytes]) -> None:
        """Download file and it opened for reading in binary mode."""
        bucket = self.config.bucket
        self.client.download_fileobj(bucket, path, dst, Config=TRANSFER_CONFIG)

    @errmap
    def upload_file(self, path: str, file: AnyFile) -> None:
        """Upload file to the given path."""
        upload_args: list = []
        upload_kwargs: dict = {"Bucket": self.config.bucket, "Key": path}
        acl = "bucket-owner-full-control"
        if isinstance(file, bytes):
            upload_func = self.client.put_object
            upload_kwargs.update(Body=file, ACL=acl)
        elif isinstance(file, str):
            upload_func = self.client.upload_file
            upload_args = [file]
            upload_kwargs.update(Config=TRANSFER_CONFIG, ExtraArgs={"ACL": acl})
        else:
            upload_func = self.client.upload_fileobj
            upload_args = [file]
            upload_kwargs.update(Config=TRANSFER_CONFIG, ExtraArgs={"ACL": acl})
        upload_func(*upload_args, **upload_kwargs)

    @errmap
    def flush_delete(self):
        """Flush pending remove operations."""
        keys = sorted(self.delete_keys)
        objects = {"Objects": [{"Key": key} for key in keys], "Quiet": True}
        resp = self.client.delete_objects(Bucket=self.config.bucket, Delete=objects)
        errs = resp.get("Errors", [])
        # TODO only clear keys that don't apper among the errors
        self.delete_keys.clear()
        if errs:
            msg = f"Bulk delete operation failed for {len(errs)} files"
            exc = errors.StorageError(msg)
            exc.errors = [f"{e['Key']}: {e['Message']}" for e in errs]
            raise exc
