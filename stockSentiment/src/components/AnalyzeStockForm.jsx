import React from "react";
import favicon from '../assets/favicon.png';
import './AnalyzeStockForm.css';
export const AnalyzeStockForm = ({analyze,setTicker}) => {
    const handleChange = (e) => {
        setTicker(e.target.value);
    }
    return (
        <div>
        <label htmlFor='ticker'>
            Stock Ticker:
        </label>
        <input onChange={(handleChange)} id='ticker' type='text' placeholder="TCKR" name='tickr' style={{textTransform: 'uppercase'}}/>
        <img className='smallIcon' src={favicon}/>
        <button onClick={()=>analyze(ticker)}>Analyze</button>
        
        </div>
    );
}