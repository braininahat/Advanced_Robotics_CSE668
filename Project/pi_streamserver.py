import io
import socket
import struct
import numpy as np
import cv2
from time import time
import sys
import orbslam2


def main(vocab_path, settings_path):

    slam = orbslam2.System(vocab_path, settings_path, orbslam2.Sensor.MONOCULAR)
    slam.set_use_viewer(True)

    print("Initializing ORB-SLAM2...\n")
    slam.initialize()
    print("Done.\n")


    # Start a socket listening for connections on 0.0.0.0:8000 (0.0.0.0 means
    # all interfaces)
    print("Starting socket server...\n")
    server_socket = socket.socket()
    server_socket.bind(('0.0.0.0', 8000))
    server_socket.listen(0)
    print("Started.\n")

    # Accept a single connection and make a file-like object out of it
    connection = server_socket.accept()[0].makefile('rb')
    print("Client connected.")
    try:
        while True:
            # Read the length of the image as a 32-bit unsigned int. If the
            # length is zero, quit the loop
            image_len = struct.unpack('<L', connection.read(struct.calcsize('<L')))[0]
            if not image_len:
                break
            # Construct a stream to hold the image data and read the image
            # data from the connection
            image_stream = io.BytesIO()
            image_stream.write(connection.read(image_len))
            # Rewind the stream, open it as an image with PIL and do some
            # processing on it
            image_stream.seek(0)
            file_bytes = np.asarray(bytearray(image_stream.read()), dtype=np.uint8)
            image = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

            tframe = time()

            if image is None:
                print("Failed to load image\n")
            return 1

            slam.process_image_mono(image, tframe)

    finally:
        slam.shutdown()
        connection.close()
        server_socket.close()
        return 0


if __name__ == '__main__':
    if len(sys.argv) != 4:
        print('Usage: python3 pi_streamserver.py path_to_vocabulary path_to_settings')
    main(sys.argv[1], sys.argv[2])
