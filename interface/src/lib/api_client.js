/**
 * @param {string} baseUrl
 * @param {string} endpoint neded start with /
 * @param {{string:any[] | number | string | undefined }} params 
 */
export async function baseGet(baseUrl, endpoint, params = undefined) {

    let url = baseUrl + endpoint;
    if (params) {

        let querys = []
        for (const key in params) {

            if (Object.hasOwnProperty.call(params, key)) {
                const param = params[key];
                if (Array.isArray(param) === true) {
                    for (const value of param) {
                        querys.push(key + '=' + encodeURIComponent(value))
                    }
                }
                else {
                    querys.push(key + '=' + encodeURIComponent(param))
                }

            }

        }
        url += '?' + querys.join('&')
    }
    const response = await fetch(url)
    if (response.ok === false) {
        return false
    }
    return await response.json()





}