import httpClient from "./httpClient";
import { useFetch } from "react-async"

const getProfileInfo = async () => {
        try {
            return await httpClient.get("/profile");
        } catch (error) {
            return null;
        }
    };


export default getProfileInfo;