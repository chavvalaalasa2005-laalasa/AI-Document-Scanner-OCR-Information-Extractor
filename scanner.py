import cv2
import easyocr
import json
import re

# Read the image
image = cv2.imread("images/sample pan card.png")

# Check if image loaded
if image is None:
    print("Image not found!")
else:
    print("Image loaded successfully!")

    # Save original image
    cv2.imwrite("output/copied_image.png", image)

    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Save grayscale image
    cv2.imwrite("output/gray_image.png", gray)

    print("Grayscale image saved successfully!")

    # Remove noise
    blur = cv2.GaussianBlur(gray, (5, 5), 0)

    # Save blurred image
    cv2.imwrite("output/blur_image.png", blur)

    print("Blur image saved successfully!")
    # Detect document edges
    edges = cv2.Canny(blur, 50, 150)

# Save edge image
    cv2.imwrite("output/edges.png", edges)

    print("Edges detected successfully!")
    # Find all contours
    contours, hierarchy = cv2.findContours(
    edges,
    cv2.RETR_EXTERNAL,
    cv2.CHAIN_APPROX_SIMPLE
    )
    print("Number of contours found:", len(contours))
    # Find the largest contour
    largest_contour = max(contours, key=cv2.contourArea)

# Draw only the largest contour
    largest = image.copy()

    cv2.drawContours(largest, [largest_contour], -1, (0,255,0), 3)

    cv2.imwrite("output/largest_contour.png", largest)

    print("Largest contour saved!")
    # Draw all contours on a copy of the original image
    contour_image = image.copy()

    cv2.drawContours(contour_image, contours, -1, (0, 255, 0), 2)

    cv2.imwrite("output/all_contours.png", contour_image)

    print("All contours saved!")
    # Threshold image
    threshold = cv2.threshold(blur, 150, 255, cv2.THRESH_BINARY)[1]

    # Save threshold image
    cv2.imwrite("output/threshold_image.png", threshold)

    print("Threshold image saved successfully!")

    # ---------------- OCR ----------------

    print("Loading EasyOCR...")

    reader = easyocr.Reader(['en'])

    result = reader.readtext("output/threshold_image.png")

    print("\nExtracted Text:\n")

    # Store extracted text
extracted_text = []

for item in result:
    print(item[1])
    extracted_text.append(item[1])

full_text = " ".join(extracted_text)

print("\nFull Text:\n")
print(full_text)

document_type = "Unknown"

if "INCOME TAX" in full_text.upper():
    document_type = "PAN Card"

elif "GOVERNMENT OF INDIA" in full_text.upper() or "AADHAAR" in full_text.upper():
    document_type = "Aadhaar Card"
pan_match = re.search(r"[A-Z]{5}[0-9]{4}[A-Z]", full_text)

if pan_match:
    pan_number = pan_match.group()
else:
    pan_number = "Not Found"
aadhaar_match = re.search(r"\d{4}\s\d{4}\s\d{4}", full_text)

if aadhaar_match:
    aadhaar_number = aadhaar_match.group()
else:
    aadhaar_number = "Not Found"
name = "Not Found"

lines = extracted_text

if document_type == "PAN Card":

    for i in range(len(lines)):

        if "GOVT" in lines[i].upper():

            if i + 1 < len(lines):

                name = lines[i + 1]

            break            

# Save as JSON

data = {
    "document_type": document_type,
    "name": name,
    "pan_number": pan_number,
    "aadhaar_number": aadhaar_number
}

with open("output/result.json", "w") as file:
    json.dump(data, file, indent=4)

print("\nStructured JSON saved successfully!")