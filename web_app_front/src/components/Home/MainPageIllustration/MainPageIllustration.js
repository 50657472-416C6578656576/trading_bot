import React, {useState} from 'react';
import './MainPageIllustration.sass';
import Logo from "../../../static/undraw_cabin_hkfr.svg";
import Illustration_1 from "../../../static/main-home-svgs/undraw_savings_re_eq4w.svg";
import Illustration_2 from "../../../static/main-home-svgs/undraw_investment_data_re_sh9x.svg";
import Illustration_3 from "../../../static/main-home-svgs/undraw_digital_currency_qpak.svg";
import Illustration_4 from "../../../static/main-home-svgs/undraw_vault_re_s4my.svg";
import Illustration_5 from "../../../static/main-home-svgs/undraw_wallet_re_cx9u.svg";


const MainPageIllustration = (props) => {
    const [isActive, setActive] = useState(false);

    const toggleClass = () => {
        setActive(true);
    };

    const phraseList = [
        "Someone stole all my credit cards, but I won't be reporting it.",
        "Ever wonder about those people who spend $2 apiece on those little bottles of Evian water? " +
        "Try spelling Evian backward.",
        "Most successful investors, in fact, do nothing most of the time.",
        "Why is the man who invests all your money called a broker?",
        "I don't read economic forecasts. I don't read the funny papers.",
        "Procrastination is like a credit card: it's a lot of fun until you get the bill.",
        "Money is not the most important thing in the world."
    ];
    const illustrationsList = [
        Illustration_1, Illustration_2, Illustration_3, Illustration_4, Illustration_5
    ]

    return (
        <div onClick={toggleClass} className={isActive ? "curtain-container active" : "curtain-container"}>
            <a href="" className='logo'>
                <img id='big-logo' height={80} src={Logo}/>
            </a>
            <div className="random-container">
                <h1 className='text-logo'>
                    Trading Bot
                </h1>
                <div className='svg-wrapper'>
                    <img id='big-illustration' height={400} src={illustrationsList[props.img_id]}/>
                    <h2 className='quote'>
                        «{phraseList[props.txt_id]}»
                    </h2>
                </div>
            </div>
        </div>
    );
};

export default MainPageIllustration;
