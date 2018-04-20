var axios = require('axios')


var baseUrl = "http://127.0.0.1:5000/"

data = {
    features: [
        [1,2,3,4,5,6,7,8,9,10]
    ]
}


axios.get(baseUrl, {
    params: {
        data: JSON.stringify(data)
    }
}).then(response=>{
    console.log(response["data"]["data"]["predict"])
})