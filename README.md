# Image Steganography and Steganalysis

## Description

This project implements both **steganography** and **steganalysis** techniques for digital images. Steganography is the practice of concealing information within other non-secret data, while steganalysis is the study of detecting hidden information.

### What is Steganography?
Steganography allows you to hide secret messages, files, or data within digital images without visibly altering the appearance of the cover image. This technique provides a covert communication channel where the existence of the hidden message is not apparent to casual observers.

### What is Steganalysis?
Steganalysis is the art and science of detecting hidden information within digital media. It involves analyzing images to determine whether they contain concealed data and potentially extracting that hidden information.

## Steganography vs Encryption

| Aspect | Steganography | Encryption |
|--------|---------------|------------|
| **Purpose** | Hide the existence of data | Protect data content |
| **Visibility** | Data appears invisible | Data is visible but unreadable |
| **Security through** | Obscurity | Mathematical algorithms |
| **Detection** | Difficult to detect hidden data exists | Easy to detect encrypted data exists |
| **Key requirement** | Optional | Always required |
| **Robustness** | Vulnerable to format changes | Resistant to data modifications |
| **Primary goal** | Covert communication | Secure communication |
| **Suspicion level** | Low (appears normal) | High (obviously protected) |

### Key Differences:
- **Steganography** focuses on hiding the fact that communication is taking place
- **Encryption** focuses on making the communication unreadable even if detected

## LSB Steganography Method

This project implements the **Least Significant Bit (LSB)** steganography technique, which is one of the most popular and widely used methods for hiding data in digital images.

### How LSB Steganography Works

LSB steganography works by replacing the least significant bits of pixel values in an image with bits from the secret message:

1. **Pixel Representation**: Each pixel in a digital image is represented by bits (e.g., 8 bits for grayscale, 24 bits for RGB)
2. **LSB Replacement**: The rightmost bit (least significant bit) of each pixel component is replaced with a bit from the secret data
3. **Minimal Impact**: Since LSBs contribute the least to the overall pixel value, changing them causes minimal visual distortion
4. **Sequential Embedding**: Message bits are embedded sequentially across the image pixels

### Example:
```
Original pixel value: 11010110 (214 in decimal)
Message bit to hide:  1
Modified pixel value: 11010111 (215 in decimal)
Visual change: Negligible (difference of ±1)
```

### Advantages of LSB Method:
- **Simple Implementation**: Easy to understand and implement
- **High Capacity**: Can hide relatively large amounts of data
- **Invisible Changes**: Modifications are imperceptible to human eye
- **Fast Processing**: Requires minimal computational resources
- **Universal Compatibility**: Works with most image formats

### Detailed LSB Example

Let's say we want to hide the message "HI" in an RGB image:

**Step 1: Convert message to binary**
```
'H' = 72 (ASCII) = 01001000 (binary)
'I' = 73 (ASCII) = 01001001 (binary)
Message bits: 0100100001001001
```

**Step 2: Original pixel values (RGB)**
```
Pixel 1: R=200 (11001000), G=150 (10010110), B=100 (01100100)
Pixel 2: R=255 (11111111), G=128 (10000000), B=64  (01000000)
Pixel 3: R=180 (10110100), G=90  (01011010), B=45  (00101101)
```

**Step 3: Embed message bits in LSBs**
```
Original: R=200 (11001000) → Modified: R=200 (11001000) [LSB=0]
Original: G=150 (10010110) → Modified: G=151 (10010111) [LSB=1]
Original: B=100 (01100100) → Modified: B=100 (01100100) [LSB=0]
...continue for remaining bits
```

**Step 4: Result**
- Visual difference: Negligible (±1 change in pixel values)
- Hidden message: Successfully embedded
- Detection: Difficult without knowing the algorithm

## LSB Variants and Parameters

This project implements **112 different LSB variants** by varying the following parameters:

### 1. **Start Position**
- **Random starting pixel**: Message embedding begins at different positions
- **Sequential embedding**: Bits are embedded consecutively from start position
- **Purpose**: Increases security by avoiding predictable patterns

### 2. **Color Channels**
- **RGB**: Use all three color channels
- **R only**: Use only Red channel
- **G only**: Use only Green channel  
- **B only**: Use only Blue channel
- **Impact**: Different channels may have varying detection rates

### 3. **Number of Bits (LSB1 to LSB8)**
- **LSB1**: Modify only 1 least significant bit
- **LSB2**: Modify 2 least significant bits
- **LSB8**: Modify up to 8 least significant bits
- **Trade-off**: Higher bits = more capacity but more distortion

### 4. **Gap Parameter**
- **Gap=1**: Embed in consecutive pixels
- **Gap=5**: Skip 4 pixels between embeddings
- **Gap=6**: Skip 5 pixels between embeddings
- **Advantage**: Spreads message across image for better concealment

### 5. **Direction**
- **Horizontal**: Process pixels row by row
- **Vertical**: Process pixels column by column
- **Pattern**: Affects embedding sequence and detection difficulty(future work)


### Applications in This Project:
- Text message hiding in PNG/BMP images
- File embedding within image containers
- Steganalysis detection of LSB-based steganography
- Performance analysis of LSB technique effectiveness

## Technologies Used

- Python
- Image processing libraries (PIL/Pillow, OpenCV)
- Machine learning algorithms for detection

## Team Members

**G. Sai Rohith (142201019)**
- Encoding implementation (Single code for all LSB variants)
- Dataset creation and preprocessing
- LSB algorithm development

**M. Rahul (142201022)**
- Architecture selection (YeNet, SRNet)
- Model training and optimization
- Decoding implementation
