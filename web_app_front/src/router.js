import React from 'react';
import {Route, Routes} from "react-router-dom";
import Home from "./components/Home/Home";
import Control from "./components/Control/Control";
import Profile from "./components/Profile/Profile";


const Router = () => {
    return (
            <Routes>
                <Route path="/" element={<Home/>}/>
                <Route path="/control" element={<Control/>}/>
                <Route path="/profile" element={<Profile/>}/>
            </Routes>
    );
};

export default Router;
