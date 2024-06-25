import os
import re
import random
import string
from flask import current_app
from werkzeug.utils import secure_filename


class FileController:
    ALLOWED_EXTENSIONS = {"image": {"png", "jpg", "jpeg", "gif", "webp"}}

    def allowed_file(self, filename: str, file_type: str):
        """Control that file is allowed

        Args:
          filename (str): Filename to control
          file_type(str): What type of file it should be, ex image, video, pdf.
        """
        return (
            "." in filename
            and filename.rsplit(".", 1)[1].lower() in self.ALLOWED_EXTENSIONS[file_type]
        )

    def create_avatar_filename(self, filename: str, user_id: int) -> str:
        filename = secure_filename(filename)
        digits = string.digits
        extension = filename.rsplit(".", 1)[1].lower()
        f_random = "".join(random.choice(digits) for i in range(4))
        l_random = "".join(random.choice(digits) for i in range(6))
        new_filename = f"uploaded-{f_random}-{user_id}-{l_random}-avatar.{extension}"

        return new_filename

    def remove_old_avatar(self, filename: str | None):
        if filename is not None:
            old_file = self.get_filename(filename)
            os.remove(
                current_app.config["UPLOAD_FOLDER"] + "/users/avatars/" + old_file
            )

    def get_filename(self, filename: str) -> str:
        match = re.search(r"[^/]+$", filename)

        if match:
            filename = match.group(0)
        return filename
