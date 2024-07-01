import React, { useState } from "react";

import deleteIcon from '@Images/delete-icon.svg';

function FileUploadPage() {

    const [files, setFiles] = useState([]);


    const handleDrop = (e) => {
        e.preventDefault();
        const droppedFiles = e.dataTransfer.files;
        if (droppedFiles.length > 0) {
            const newFileCategories = Array.from(droppedFiles).map(file => ({ file, category: '' }));
            setFiles((prevFileCategories) => [...prevFileCategories, ...newFileCategories]);
        }
    };

    const handleFileSelect = (e) => {
        const selectedFiles = e.target.files;
        if (selectedFiles.length > 0) {
            const newFileCategories = Array.from(selectedFiles).map(file => ({ file, category: '' }));
            setFiles((prevFileCategories) => [...prevFileCategories, ...newFileCategories]);
        }
    };

    async function uploadFiles(callback) {
        if (files.some(file => file.category == '')) return callback(new Error('All files must have a category.'));
        const formData = new FormData();
        let categoriesArray = [];
        files.forEach((file) => {
            formData.append('files', file.file);
            categoriesArray.push(file.category);
        });
        formData.append('categories', JSON.stringify(categoriesArray));
        try {
            const response = await fetch(`${process.env.REACT_APP_API_URL}/knowledge_manager/`, {
                method: 'POST',
                body: formData,
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const data = await response.json();
            callback(null, data);
        } catch (error) {
            callback(error);
        }
    }

    const callAPI = async () => {
        console.log("called api")
        uploadFiles((error, data) => {
            if (error) {
                console.error('An error occurred:', error);
            } else {
                console.log('Received data:', data);
            }
        });
    };

    return (
        <div className="file-upload">
            <div
                className="file-upload-box"
                onDrop={handleDrop}
                onDragOver={(e) => e.preventDefault()}
            >
                Drag and drop your files here
            </div>
            <input
                type="file"
                id="upload-btn"
                accept=".docx"
                onChange={handleFileSelect}
                multiple
                hidden
            />
            <div className="file-upload-names">
                {files.map((file, index) => (
                    <div className="file-upload-names-wrapper" key={index}>
                        <div className="file-upload-names-label">{file.file.name}</div>
                        <input
                            className="file-upload-names-input"
                            type="text"
                            placeholder="Enter category"
                            onChange={(e) => {
                                setFiles((files) => files.map((file, i) => i === index ? { ...file, category: e.target.value } : file));
                            }}
                        />
                        <img
                            className="file-upload-names-icon"
                            src={deleteIcon} alt="Delete"
                            onClick={() => setFiles((prevFiles) => prevFiles.filter((_, i) => i !== index))}
                        />
                    </div>
                ))}
            </div>
            <label className="file-upload-select-btn" htmlFor="upload-btn">Browse files</label>
            <button className="file-upload-btn" onClick={callAPI}>Upload</button>
        </div>
    )
}

export default FileUploadPage;