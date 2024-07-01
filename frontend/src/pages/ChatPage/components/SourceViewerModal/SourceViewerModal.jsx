import React, { useEffect, useState, useRef } from 'react';
import Modal from 'react-modal';

import PDFObject from 'pdfobject';

Modal.setAppElement('#root');

const SourceViewerModal = ({ isModalOpen, closeModal, source }) => {
    const [pdfUrl, setPdfUrl] = useState(null);
    const pdfContainer = useRef(null);

    // useEffect(() => {
    //     if (isModalOpen && source) {
    //         fetch('pdf _url')
    //             .then(response => {
    //                 if (!response.ok) {
    //                     throw new Error('Network response was not ok');
    //                 }
    //                 if (response.headers.get('Content-Type') !== 'application/pdf') {
    //                     throw new Error('Response is not a PDF');
    //                 }
    //                 return response.blob();
    //             })
    //             .then(blob => {
    //                 const url = URL.createObjectURL(blob); 
    //                 setPdfUrl(url);
    //             })
    //             .catch(error => {
    //                 console.error('There has been a problem with your fetch operation:', error);
    //             });
    //     }
    // }, [isModalOpen, source]);

    useEffect(() => {
        if (pdfUrl && pdfContainer.current) {
            PDFObject.embed(pdfUrl, pdfContainer.current);
        }
    }, [pdfUrl]);

    return (
        <Modal
            isOpen={isModalOpen}
            onRequestClose={closeModal}
            style={{
                overlay: {
                    backgroundColor: 'rgba(0, 0, 0, 0.5)'
                },
                content: {
                    position: 'absolute',
                    top: '50%',
                    left: '50%',
                    right: 'auto',
                    bottom: 'auto',
                    marginRight: '-50%',
                    width: '80%',
                    height: '80%',
                    transform: 'translate(-50%, -50%)'
                }
            }}
        >
            <div ref={pdfContainer} style={{ width: '100%', height: '100%' }} />
        </Modal>
    );
};

export default SourceViewerModal;