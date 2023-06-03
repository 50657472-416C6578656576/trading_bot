import React, {useState} from 'react';
import './Home.sass';
import Atree from '../../static/Atree.svg';
import MainPageIllustration from "./MainPageIllustration/MainPageIllustration";


const Home = () => {
    const txt_id = Math.floor(Math.random() * 7);
    const img_id = Math.floor(Math.random() * 5);


    return (
        <div className="Home">
            <MainPageIllustration txt_id={txt_id} img_id={img_id}/>
            <div className="home-wrapper">
                <div className="text-block">
                    <p>
                        This project implements trading on the Binance platform using different strategies
                        such as RSI, BOLL, EMA, MACD.
                        Basically, it's just a bot for trading on the Binance, so
                        you will need a personal API token and a secret to use it. Take your risk :)
                    </p>
                </div>
                <div className="TreeDeco">
                    <img id='Atree' height={180} src={Atree}/>
                </div>
            </div>
        </div>
    );
};

export default Home;
