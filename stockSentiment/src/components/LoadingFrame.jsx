import React, { useEffect } from "react";
import { useState } from "react";

export const LoadingFrame = () => {
    const [message, setMessage] = useState('Loading...');

    const possibleMessage = ['Calculating feelings...', 'Counting dollars...',"Lots of strong feelings here...","Scraping the web...",
    "Reading sentiments...","Must be a popular ticker...","Almost partially done...", "Browsing Reddit...", "Consulting wall street bets..."];
    useEffect(() =>{
        const interval = setInterval(() => {
            setMessage(possibleMessage[Math.floor(Math.random() * possibleMessage.length)]);
        }, 1500);
        return () => clearInterval(interval);
        },[]);
    

    return (
        <div>
            <h3>{message}</h3>
        </div>
    );
}