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
Returns all processed images (including failed ones) and their metadata.

GET /api/images/{image_id}
Returns metadata and caption for a specific image, the time an image was processed is at GMT+00.

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
For example, to upload an image, the user can first expand the POST /upload.
<img width="919" height="83" alt="image" src="https://github.com/user-attachments/assets/6faa6b02-87e7-4fef-afef-1a5ea3c2de15" />
The user can then press "Try it out" and upload thier image.
<img width="1823" height="288" alt="image" src="https://github.com/user-attachments/assets/a2ff6e96-89d0-458e-aa56-263043a5e870" />

<img width="1836" height="588" alt="image" src="https://github.com/user-attachments/assets/bf18b8c7-3cf2-451a-986b-69eff1192889" />
After uploading, the user can press execute to start processing the image.
<img width="1816" height="586" alt="image" src="https://github.com/user-attachments/assets/46be05c4-c94e-45b5-ad10-3fac47ce599a" />
The user can then see the response below:
<img width="1776" height="583" alt="image" src="https://github.com/user-attachments/assets/e311b5a7-c8bd-49d8-b997-9bce7ba59e5d" />

Processing Pipeline Explanation:

When an image is uploaded, the system performs the following steps:
Step 1 — File Validation
Verifies the file using Pillow (magic-byte validation)
Rejects unsupported formats
Logs invalid attempts

Step 2 — Metadata Extraction
Extracts width, height, format, and file size
Generates a unique UUID for the image

Step 3 — Thumbnail Generation
Medium thumbnail → 50% of original dimensions
Small thumbnail → 25% of original dimensions
Saves thumbnails locally

Step 4 — AI Caption Generation
Uses Salesforce BLIP image captioning model
Generates a natural language description
Adds caption to API response

Step 5 — Logging
Logs upload attempts
Logs processing success or failure
Logs caption generation
Stores logs in logs/app.log

Step 6 — Statistics Tracking
Tracks total uploads
Tracks failed uploads
Calculates success rate
Calculates average processing time
