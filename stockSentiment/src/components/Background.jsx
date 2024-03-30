import React from "react";
import upArrow from '../assets/upArrow.png';
import './Background.css'

export const Background = () => {

    return (
        <div className="center">
          <img className="background" src={upArrow}></img>
            <div className="hider"></div>
        </div>
    );
}