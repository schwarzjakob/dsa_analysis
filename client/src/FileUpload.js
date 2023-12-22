// FileUpload.js
import React, { useState } from 'react';
import axios from 'axios';
// import { useNavigate } from 'react-router-dom'; // Import useNavigate
import './App.css'
import Header from './Header.js'

function FileUpload() {
    const [file, setFile] = useState(null);
    // const navigate = useNavigate(); // Create an instance of useNavigate

    const handleFileChange = (e) => {
        setFile(e.target.files[0]);
    }

    const handleSubmit = async (e) => {
        e.preventDefault();
        const formData = new FormData();
        formData.append('file', file);

        try {
            await axios.post('http://127.0.0.1:5000/upload', formData, {
                headers: {
                    'Content-Type': 'multipart/form-data'
                }
            });
            alert('File uploaded successfully');
        } catch (error) {
            alert('Error uploading file');
        }
    }

    return (
        <><div>
            <Header />
        </div>
            <div className="main-container">
                <div className="form-container">
                    <div>
                        <form onSubmit={handleSubmit}>
                            <input type="file" onChange={handleFileChange} />
                            <button type="submit">Upload</button>
                        </form>
                    </div>
                </div>
            </div></>
    );
}

export default FileUpload;
