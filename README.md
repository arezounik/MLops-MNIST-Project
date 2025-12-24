# MNIST MLOps Project 🚀

This project is a containerized Deep Learning application for MNIST digit classification, built with PyTorch and MLflow.

## How to Run and Test

1. **Start the Application:**



   *Building from Source*

      1.Run the following command in your terminal:
        ```bash
        docker-compose up --build



   *Running with Docker Hub Image*

      1.Open docker-compose.yml
      2.Comment out the build line:
	```bash
	build: .
      3.Uncomment the image line:
	```bash 
	# image: arezounik/mlops-app:dev
      4.Run the following command in your terminal:
	```bash
        docker-compose up


2. **Access the API Documentations**:

Once the containers are up and running, you can access the interactive API documentation (Swagger UI) to test the endpoints at:


http://localhost:8000/docs


http://localhost:8001/docs
