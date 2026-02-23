This project is a RESTful Image Processing API built using FastAPI and implemented using Python 3.11.6.

The system allows users to upload JPG and PNG images, automatically performs validation and processing, generates proportional thumbnails, and uses an AI vision model to produce an image caption.

Key features include:
Image upload (JPG & PNG only)
Magic-byte validation (prevents renamed file spoofing)
Proportional thumbnail generation (50% and 25% of original size)
AI-powered image captioning (BLIP model)
Processing statistics endpoint
Structured logging

Installation Steps:
1. Clone the repository via "git clone https://github.com/johnsinned/Image_Processer.git" in your bash terminal and cd into the folder via "cd Image_Processer".
2. Create a virtual environment via "python -m venv venv" and activate it using "venv\Scripts\activate".
3. Install the required dependencies using "pip install -r requirements.txt".
4. To start the server, execute "uvicorn app.main:app --reload" from the root directory of the project and the server will start at http://127.0.0.1:8000 where the web GUI used to interact with it is at http://127.0.0.1:8000/docs.
<img width="1899" height="739" alt="image" src="https://github.com/user-attachments/assets/af57c224-a4ab-475c-a6a7-d55fd51c3dd5" />


API Documentation:
POST /upload
Uploads an image and processes it.

GET /api/images
Returns all processed images (including failed ones).

GET /api/images/{image_id}
Returns metadata and caption for a specific image.

GET /api/images/{image_id}/thumbnails/{size}
Retrieves a generated thumbnail where the medium and small thumbnails are 50% and 25% of the original size uploaded respectively.

GET /api/stats
Returns processing statistics which include:
Total uploads
Failed uploads
Success rate
Average processing time

Example usage:
User can use the web GUI at http://127.0.0.1:8000/docs to directly upload images and return processed images and their thumbnails and etc.
<img width="1824" height="614" alt="image" src="https://github.com/user-attachments/assets/07347811-6885-4947-b464-971fb76daa51" />
