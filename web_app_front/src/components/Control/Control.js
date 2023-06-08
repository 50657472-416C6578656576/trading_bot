import React, {useEffect, useState} from 'react';
import getProfileInfo from "../../getProfileInfo";
import Atree from "../../static/Atree.svg";
import httpClient from "../../httpClient";

const Control = () => {
    const [current_balance, setCurrentBalance] = useState("Unknown");

    const startTrading = async () => {
        await httpClient.post("/start_trading", {

        });
    };
    const stopTrading = async () => {
        await httpClient.post("/stop_trading");
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
                    <h1>Current balance: {current_balance}</h1>
                    <button type="button" onClick={() => startTrading()}>start trading</button>
                    <button type="button" onClick={() => stopTrading()}>stop trading</button>
                </div>
                <div className="TreeDeco">
                    <img id='Atree' height={180} src={Atree}/>
                </div>
            </div>
        </div>
    );
};

export default Control;
