import React, {useEffect, useState} from 'react';
import getProfileInfo from "../../getProfileInfo";
import Atree from "../../static/Atree.svg";
import httpClient from "../../httpClient";

const Control = () => {
    const [current_balance, setCurrentBalance] = useState("Unknown");

    const [strategy, setStrategy] = useState("");
    const [symbol, setSymbol] = useState("");
    const [timeframe, setTimeframe] = useState("");

    const startTrading = async () => {
        try {
            const response = await httpClient.post("/start_trading", {
                strategy,
                symbol,
                timeframe
            });
            alert("Trading started");
        } catch {
            alert("Something went wrong")
        }
    };
    const stopTrading = async () => {
        await httpClient.post("/stop_trading");
        alert("Trading stopped");
    };

    useEffect(async () => {
        const response = await getProfileInfo();
        if (response === null) {
            window.location.href = "/profile";
        }
        try {
            const response = await httpClient.get("/balance");
            setCurrentBalance(response.data.balance);
        } catch {}
    }, []);
    return (
        <div className="Control">
            <div className="control-wrapper">
                <div className="text-block">
                    <form>
                        <h1>Current balance: {current_balance}</h1>
                        <div>
                            <input
                                type="text"
                                value={strategy}
                                onChange={(e) => setStrategy(e.target.value)}
                                id=""
                                placeholder="strategy"
                            />
                        </div>
                        <div>
                            <input
                                type="text"
                                value={symbol}
                                onChange={(e) => setSymbol(e.target.value)}
                                id=""
                                placeholder="symbol"
                            />
                        </div>
                        <div>
                            <input
                                type="text"
                                value={timeframe}
                                onChange={(e) => setTimeframe(e.target.value)}
                                id=""
                                placeholder="timeframe"
                            />
                        </div>
                        <br/>
                        <button type="button" onClick={() => startTrading()}>start trading</button>
                    </form>
                    <br/>
                    <form>
                    <button type="button" onClick={() => stopTrading()}>stop trading</button>
                    </form>
                </div>
                <div className="TreeDeco">
                    <img id='Atree' height={180} src={Atree}/>
                </div>
            </div>
        </div>
    );
};

export default Control;
