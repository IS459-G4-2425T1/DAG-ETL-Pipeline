FROM public.ecr.aws/lambda/python:3.9

# Install Chrome and dependencies
RUN yum install -y unzip curl && \
    curl -Lo "/tmp/chromedriver.zip" "https://chromedriver.storage.googleapis.com/114.0.5735.90/chromedriver_linux64.zip" && \
    curl -Lo "/tmp/chrome-linux.zip" "https://www.googleapis.com/download/storage/v1/b/chromium-browser-snapshots/o/Linux_x64%2F1135561%2Fchrome-linux.zip?alt=media" && \
    unzip /tmp/chromedriver.zip -d /opt/ && \
    unzip /tmp/chrome-linux.zip -d /opt/ && \
    rm /tmp/chromedriver.zip /tmp/chrome-linux.zip && \
    yum install -y atk cups-libs gtk3 libXcomposite alsa-lib \
    libXcursor libXdamage libXext libXi libXrandr libXScrnSaver \
    libXtst pango at-spi2-atk libXt xorg-x11-server-Xvfb \
    xorg-x11-xauth dbus-glib dbus-glib-devel nss mesa-libgbm && \
    chmod 755 /opt/chromedriver && \
    chmod -R 755 /opt/chrome-linux

# Set up working directory
WORKDIR ${LAMBDA_TASK_ROOT}

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt --no-cache-dir

# Copy all your function code
COPY main.py .
COPY process_data.py .

# Set the Chrome driver path and other environment variables
ENV CHROMEDRIVER_PATH=/opt/chromedriver
ENV CHROME_BINARY_PATH=/opt/chrome-linux/chrome
ENV PATH="${PATH}:/opt"
ENV PYTHONPATH="${LAMBDA_TASK_ROOT}"

# Set the Lambda handler
CMD [ "main.lambda_handler" ]