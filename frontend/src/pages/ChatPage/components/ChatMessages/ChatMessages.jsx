import React, { useState } from 'react';
import SourceViewerModal from '../SourceViewerModal';

import profilePic from '@Images/profile-pic.svg';
import avatarPic from '@Images/avatar-pic.png';

function ChatMessages({ messages = [], isLoading, handleCategoryClick }) {
    const [modalIsOpen, setModalIsOpen] = useState(false);
    const [selectedSource, setSelectedSource] = useState(null);
    const [selectedCategories, setSelectedCategories] = useState([]);

    function openModal() {
        setModalIsOpen(true);
    }

    function closeModal() {
        setModalIsOpen(false);
    }

    function handleSourceClick(source) {
        // openModal();
        setSelectedSource(source);
    }

    function onCategoryClick(categoryId, index) {
        if (!isCategorySelected(index)) {
            setSelectedCategories(prevCategories => [...prevCategories, { categoryId, index }]);
            handleCategoryClick(categoryId);
        }
    }

    function isCategorySelected(index, categoryId) {
        if (categoryId === undefined) {
            return selectedCategories.some(category => category.index === index);
        } else {
            return selectedCategories.some(category => category.index === index && category.categoryId === categoryId);
        }
    }

    function shouldDisplaySources(data) {
        return data.sender === 'Assistant' &&
            data.sources &&
            data.sources.length > 0 &&
            !(isLoading && (data.id === messages[messages.length - 1].id)) &&
            data.sources.some(source => source.filename);
    }

    return (
        <div className="chat-messages">
            {messages.map((data, msgIndex) => (
                <div key={msgIndex} className={"chat-message" + (data.sender === 'You' ? '-user' : '-dtc')}>
                    <div className="chat-message-avatar">
                        <img src={data.sender == 'You' ? profilePic : avatarPic} alt="Profile Picture" className="chat-message-avatar-pic" />
                    </div>
                    <div className="chat-message-wrapper">
                        <span className="chat-message-author">{data.sender == 'You' ? "You" : 'DT Companion'}</span>
                        {data.message.map((chunk, index) => (
                            <span key={index} className="chat-message-text">{chunk}</span>
                        ))}
                        {shouldDisplaySources(data) &&
                            <div className="chat-message-sources">
                                <span className="chat-message-sources-title">Sources:</span>
                                {data.sources.map((source, index) => (
                                    (<div
                                        key={index}
                                        className="chat-message-source"
                                        onClick={() => handleSourceClick(source)}
                                        style={{ animationDelay: index * 50 + 'ms' }}
                                    >
                                        <span className="chat-message-source-filename">{source.filename}</span>
                                        <span className="chat-message-source-page"> Page {source.page}</span>
                                    </div>
                                    )
                                ))}
                            </div>
                        }
                        {data && data.categoriesList && data.categoriesList.length > 0 && (
                            <div className="chat-message-categories">
                                {data.categoriesList.map((category, index) => (
                                    <div
                                        key={index}
                                        className={`chat-message-category ${isCategorySelected(msgIndex, category.category_id) ?
                                            "selected"
                                            :
                                            isCategorySelected(msgIndex) ? "inactive" : ""}`
                                        }
                                        style={{ animationDelay: index * 50 + 'ms' }}
                                        onClick={() => onCategoryClick(category.category_id, msgIndex)}
                                    >
                                        <span className="chat-message-category-name">{category.category_id}</span>
                                    </div>
                                ))}
                            </div>
                        )}
                    </div>
                </div>
            ))}
            <SourceViewerModal isModalOpen={modalIsOpen} closeModal={closeModal} source={selectedSource} />
        </div>
    );
}

export default ChatMessages;