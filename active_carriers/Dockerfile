FROM public.ecr.aws/lambda/python:3.9

# Install Chrome and dependencies
RUN yum install -y unzip && \
    curl -Lo "/tmp/chromedriver.zip" "https://chromedriver.storage.googleapis.com/114.0.5735.90/chromedriver_linux64.zip" && \
    curl -Lo "/tmp/chrome-linux.zip" "https://www.googleapis.com/download/storage/v1/b/chromium-browser-snapshots/o/Linux_x64%2F1135561%2Fchrome-linux.zip?alt=media" && \
    unzip /tmp/chromedriver.zip -d /opt/ && \
    unzip /tmp/chrome-linux.zip -d /opt/ && \
    rm /tmp/chromedriver.zip /tmp/chrome-linux.zip && \
    yum install -y atk cups-libs gtk3 libXcomposite alsa-lib \
    libXcursor libXdamage libXext libXi libXrandr libXScrnSaver \
    libXtst pango at-spi2-atk libXt xorg-x11-server-Xvfb \
    xorg-x11-xauth dbus-glib dbus-glib-devel nss mesa-libgbm

# Set up working directory
WORKDIR ${LAMBDA_TASK_ROOT}

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy your function code
COPY main.py .

# Set the Chrome driver path
ENV CHROMEDRIVER_PATH=/opt/chromedriver
ENV CHROME_BINARY_PATH=/opt/chrome-linux/chrome

# Set the Lambda handler
CMD [ "main.lambda_handler" ]