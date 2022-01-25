const axios = require("axios");

const api_key = process.env.api_key;
const domain = process.env.domain;

export async function getUser() {
    await axios
        .get(
            "https://" + domain + "/api/v1/user/?username=" + username + "&api_key=" + api_key
        )
        .then((response) => {
            return response.data.objects;
        })
        .catch((err) => {
            console.log(err);
        });
    return result;
}

export async function getAllUsers() {
    await axios
        .get(
            "https://" + domain + "/api/v1/user/?username=" + "&api_key=" + api_key
        )
        .then((response) => {
            return response.data.objects;
        })
        .catch((err) => {
            console.log(err);
        });
    return result;
}

export async function createUser(user) {
    await axios
        .post(
            "https://" + domain + "/api/v1/user/?username=" + "&api_key=" + api_key, user
        )
        .then((response) => {
            return response.data.objects;
        })
        .catch((err) => {
            console.log(err);
        });
    return result;
}

export async function sumbitReport(username, report) {
    await axios
        .post(
            "https://" + domain + "/api/v1/user/?username=" + username + "&api_key=" + api_key, report
        )
        .then((response) => {
            return response.data.objects;
        })
        .catch((err) => {
            console.log(err);
        });
    return result;
}