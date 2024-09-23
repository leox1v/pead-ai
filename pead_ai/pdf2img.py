import fitz
import tempfile
from pathlib import Path
from streamlit.runtime.uploaded_file_manager import UploadedFile

class Converter:
    def __init__(self, uploaded_file: UploadedFile, zoom: int = 5):
        self.uploaded_file = uploaded_file
        self.zoom = zoom
        self.img_folder = Path(tempfile.mkdtemp())

    def pdf_to_jpg(self):
        """
        Convert the uploaded PDF file to JPEG images.

        Reads the uploaded PDF file and converts each page into a separate JPEG image.
        The converted JPEG images are saved in a temporary directory.
        """
        with fitz.open(stream=self.uploaded_file.read(), filetype="pdf") as doc:
            matrix = fitz.Matrix(self.zoom, self.zoom)
            for page_num, page in enumerate(doc, start=1):
                pix = page.get_pixmap(matrix=matrix)
                pix.save(self.img_folder / f"page_{page_num}.jpg")

    @property
    def image_paths(self):
        """Return a list of paths to the converted images."""
        return sorted(self.img_folder.glob("*.jpg"))

    def cleanup(self):
        """Remove the temporary directory and its contents."""
        import shutil
        shutil.rmtree(self.img_folder)