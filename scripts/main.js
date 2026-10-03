const ip_input = document.getElementById("connect-ip")
const port_input = document.getElementById("connect-port")
const username_input = document.getElementById("connect-username")
const connect_button = document.getElementById("connect-button")

let ws;

function send(ws, d) {
    console.log(d)
    ws.send(JSON.stringify(d))
}

connect_button.onclick = function () {
    const ip = ip_input.value
    const port = port_input.value

    if (!ip || !port) {
        alert("please input an ip and port")
    }

    try {
        ws = new WebSocket(`ws://${ip}:${port}`)
    } catch (e) {
        console.error(e)
        alert("An error occourred whilst connecting to the server, check the console")
    }

    ws.onopen = function (event) {
        console.log("Connected to the server")

        send(ws, { "op": 2, "d": { "username": username_input.value } })
    }

    ws.onmessage = function (event) {
        console.log(event.data)
    }

    ws.onclose = function (event) {
        console.log(`Disconnected from server ${event.code}`)
        alert("Disconnected, check console")
    }

    ws.onerror = function (error) {
        console.log(`Websocket error: `)
        console.log(error)
        alert("An error occourred, check the console")
    }
}
