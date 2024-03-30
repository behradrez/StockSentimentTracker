import { useState } from 'react'
import reactLogo from './assets/react.svg'
import bull from './assets/wsBull.jpg'
import './App.css'
import './components/AnalyzeStockForm'
import { AnalyzeStockForm } from './components/AnalyzeStockForm'
import { LoadingFrame } from './components/LoadingFrame'
import { Background } from './components/Background'


async function analyzeStock(ticker,{setPositive,setLoading,setError}){
  setLoading(true);
  var url = "http://127.0.0.1:5000/analyze/percent/"+ticker;
  var method = "GET";
  try{
    const response = await fetch(url, {method: method});
    const data = await response.json();
    console.log(response);
    console.log(data);  
    setPositive(data.positive);
  }catch(e){
    setPositive(false);
    setError(""+e);
  }
  setLoading(false);
}
  
function App() {
  const [positive, setPositive] = useState(false);
  const [loading,setLoading] = useState(false);
  const [ticker, setTicker] = useState('AAPL');
  const [error, setError] = useState(false);


  return (
    <>
      <div>
      <a href="https://behradrez.github.io/">
        <img className="image" src={bull}></img>
      </a>
      </div>
      <h1>Stock Sentiment Tracker</h1>
      <AnalyzeStockForm setTicker={setTicker} analyze={()=>analyzeStock(ticker,{setPositive,setLoading,setError})}/>
      
      {loading &&
        <LoadingFrame></LoadingFrame>}

      {error &&
        <h3>Encountered an exception: {error}</h3>}

      {!loading && positive &&
        <h3>Overall sentiment for {ticker} is {positive}% positive, and {100-positive}% negative</h3>}

      {!positive && !error &&
        <h3>Enter a ticker to find out how people feel about it!</h3>}

    </>
  )
}

export default App
