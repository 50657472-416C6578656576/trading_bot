import getProfileInfo from "./getProfileInfo";

async function authorized() {
        const info = await getProfileInfo();
        return info !== null;
    }

export default authorized;