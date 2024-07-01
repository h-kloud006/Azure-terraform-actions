import React, { useState, useRef, useEffect } from 'react';

import ChatMessages from './components/ChatMessages';


const tempPrompts = [
    { text: "What are five policy types?" },
    { text: "Where should I get approval for policy type Integrity Code (IC)?" },
    { text: "Where should I get approval for policy type Corporate policies (A policies)?" },
    { text: "List all Policy types which have scope of Application as Restricted to management levels?" }
]

function ChatPage() {

    const [input, setInput] = useState('');
    const [isInputDisabled, setIsInputDisabled] = useState(false);
    const [responses, setResponses] = useState([]);
    const ws = useRef(null);
    const messagesEndRef = useRef(null);

    const [reconnectAttempts, setReconnectAttempts] = useState(0);
    const maxReconnectAttempts = 5;

    useEffect(() => {
        setupWebSocket(); // Setup WebSocket on component mount

        return () => {
            if (ws.current.readyState === WebSocket.OPEN) {
                ws.current.close(); // Close WebSocket on component unmount
            }
        };
    }, []);

    useEffect(() => {
        messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    }, [responses]);

    const setupWebSocket = () => {
        ws.current = new WebSocket(`${process.env.REACT_APP_WS_URL}/chat/`);
        let ongoingStream = null; // To track the ongoing stream's ID

        ws.current.onopen = () => {
            console.log("WebSocket connected!");
            setReconnectAttempts(0); // Reset reconnect attempts on successful connection
        };

        ws.current.onmessage = (event) => {
            const data = JSON.parse(event.data);
            let sender = 'Assistant';

            // Handle different types of events from the WebSocket
            if (data.event_type === 'on_parser_start') {
                // When a new stream starts
                ongoingStream = { id: data.answer_id };
                setResponses(prevResponses => [...prevResponses, { sender, message: [], id: data.answer_id }]);
            } else if (data.event_type === 'answer_init' && ongoingStream && data.answer_id === ongoingStream.id) {
                // console.log("answer_init",data)
                setResponses(prevResponses => prevResponses.map(msg =>
                    msg.id === data.answer_id ? { ...msg, sources: data.sources } : msg));
            } else if (data.event_type === 'on_parser_stream' && ongoingStream && data.answer_id === ongoingStream.id) {
                // During a stream, appending new chunks of data
                setResponses(prevResponses => prevResponses.map(msg =>
                    msg.id === data.answer_id ? { ...msg, message: [...msg.message, data.answer_part] } : msg));
            } else if (data.event_type === 'categories_list') {
                setResponses(prevResponses => [...prevResponses, { message: ['For more detailed information, please select a category or provide a more specific query.'], categoriesList: data.categories }]);
            } else if (data.event_type === 'on_parser_end') {
                setTimeout(() => setIsInputDisabled(false), 2000);
            }
        };

        ws.current.onerror = (event) => {
            console.error("WebSocket error observed:", event);
        };

        ws.current.onclose = (event) => {
            if (event.code === 1000) return; // Normal closure (connection closed successfully)
            console.log(`WebSocket is closed now. Code: ${event.code}, Reason: ${event.reason}`);
            handleReconnect();
        };
    }

    const handleReconnect = () => {
        if (reconnectAttempts < maxReconnectAttempts) {
            let timeout = Math.pow(2, reconnectAttempts) * 1000; // Exponential backoff
            setTimeout(() => {
                setupWebSocket(); // Attempt to reconnect
            }, timeout);
        } else {
            console.log("Max reconnect attempts reached, not attempting further reconnects.");
        }
    }

    function handlePromptClick(message) {
        const userMessage = { sender: "You", message: [message] };
        setIsInputDisabled(true);
        ws.current.send(JSON.stringify({ message: message, request_type: 'query'}));
        setResponses([userMessage]);
    }

    const handleSubmit = (e) => {
        e.preventDefault();
        setIsInputDisabled(true);
        const userMessage = { sender: "You", message: [input], request_type: 'query'};
        setResponses(prevResponses => [...prevResponses, userMessage]);
        ws.current.send(JSON.stringify({ message: input, request_type: 'query' }));
        setInput('');
    }

    function handleCategoryClick(categoryId) {
        const userMessage = { 'category_id': categoryId, message: [], request_type: 'category_selection', previous_query: responses[responses.length - 2].message[0]};
        ws.current.send(JSON.stringify(userMessage));
    }

    return (
        <div className="chat-page">
            <div className="chat-page-messages">
                {responses.length === 0 ?
                    <div className="chat-page-prompts">
                        <div className="chat-page-prompts-wrapper">
                            {tempPrompts.map((prompt, index) => (
                                <div key={index} className="chat-page-prompts-prompt" onClick={() => handlePromptClick(prompt.text)}>
                                    <p className="chat-page-prompts-prompt-text">{prompt.text}</p>
                                </div>
                            ))}
                        </div>
                    </div>
                    :
                    <ChatMessages messages={responses} isLoading={isInputDisabled} handleCategoryClick={handleCategoryClick}/>
                }
                <div ref={messagesEndRef} />
            </div>
            <div className="chat-page-input">
                <input
                    className="chat-page-input-field"
                    type="text"
                    placeholder="Type a message"
                    value={input}
                    onChange={(e) => setInput(e.target.value)}
                    onKeyDown={(e) => e.key === 'Enter' && handleSubmit(e)}
                    disabled={isInputDisabled}
                />
                <button className="chat-page-input-send-btn" onClick={handleSubmit}>
                    <svg className="chat-page-input-send-icon" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                        <path d="M11.5003 12H5.41872M5.24634 12.7972L4.24158 15.7986C3.69128 17.4424 3.41613 18.2643 3.61359 18.7704C3.78506 19.21 4.15335 19.5432 4.6078 19.6701C5.13111 19.8161 5.92151 19.4604 7.50231 18.7491L17.6367 14.1886C19.1797 13.4942 19.9512 13.1471 20.1896 12.6648C20.3968 12.2458 20.3968 11.7541 20.1896 11.3351C19.9512 10.8529 19.1797 10.5057 17.6367 9.81135L7.48483 5.24303C5.90879 4.53382 5.12078 4.17921 4.59799 4.32468C4.14397 4.45101 3.77572 4.78336 3.60365 5.22209C3.40551 5.72728 3.67772 6.54741 4.22215 8.18767L5.24829 11.2793C5.34179 11.561 5.38855 11.7019 5.407 11.8459C5.42338 11.9738 5.42321 12.1032 5.40651 12.231C5.38768 12.375 5.34057 12.5157 5.24634 12.7972Z"
                            strokeWidth="2"
                            strokeLinecap="round"
                            strokeLinejoin="round"
                        />
                    </svg>
                </button>
            </div>
        </div>
    );
}

export default ChatPage;
