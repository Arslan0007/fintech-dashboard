# 1. Use a lightweight Python OS
FROM python:3.9-slim

# 2. Create a working directory inside the container
WORKDIR /app

# 3. Copy our "Recipe" (requirements) first
COPY requirements.txt .

# 4. Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copy the rest of the code
COPY . .

# 6. Open the port for business
EXPOSE 5000

# 7. The command to start the server
CMD [ "python", "app.py" ]