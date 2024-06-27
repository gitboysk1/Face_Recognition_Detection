import React, { useState } from "react";
import axios from "axios";
import gif from './image/face_verify.gif';
import './Gif.css';

const Gif = () => {
    const [uploadedImage, setUploadedImage] = useState(null);
    
    const [person,setPerson]=useState()
    const [sentiment,setSentiment]=useState()

    const handleImageUpload = (event) => {
        const file = event.target.files[0];
        setUploadedImage(file);
        console.log(file)
        // Create a new FileReader instance
        const reader = new FileReader();
          // Define a function to be executed when the file is read
          reader.onload = () => {
            // Log the result (base64 encoded image data) to the console
            console.log(reader.result);
        };
         // Read the contents of the file as a data URL
         reader.readAsDataURL(file);

        console.log("here is our image ",uploadedImage)
    };
  
    const handleShowButtonClick = async () => {
        if (!uploadedImage) {
            alert("Please upload an image.");
            return;
        }

        const formData = new FormData();
        formData.append("image", uploadedImage);

        try {
            console.log(" TRYING TO SEND DATA SENT TO BACKEND ")
            const response = await axios.post("http://127.0.0.1:5000/detect_emotion", formData, {
                headers: {
                    "Content-Type": "multipart/form-data"
                }
            });
            
           
            console.log(response)
            setPerson(response.data[0].person)
            setSentiment(response.data[0].emotion)
            console.log(response.data[0].emotion)
            console.log(response.data[0].person)
        } catch (error) {
            console.error("Error:", error);
        }
    };

    return (
        <div className="mainBox">
            <div className="text_part">
                <h1>Emotion Detection and Face Recognition </h1>
                <div className="search-container">
                    <input id="fileChoose"  type="file" accept="image/*" onChange={handleImageUpload} />
                    <button id="show_button" onClick={handleShowButtonClick}>Detect</button>
                </div>
               <div className="sentiment-result">
                    { <pre>Emotion: {sentiment}     Person: {person} </pre>}
                </div>
                <div className="pImage">{uploadedImage && (
                        <img src={URL.createObjectURL(uploadedImage)} height={400} alt="Uploaded Image" />
                    )}</div>
                
            </div>
            <div className="gif_part">
                <img src={gif} alt="Sample GIF" />
                
            </div>
        </div>
    );
};

export default Gif;
