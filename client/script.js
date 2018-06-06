let screen, initWidth, initHeight, host;
let socket;

function debounce(func, wait, immediate) {
	let timeout;
	return function() {
		let context = this, args = arguments;
		let later = function() {
			timeout = null;
			if (!immediate) func.apply(context, args);
		};
		let callNow = immediate && !timeout;
		clearTimeout(timeout);
		timeout = setTimeout(later, wait);
		if (callNow) func.apply(context, args);
	};
};

function screenUpdate(){
    let binary = reader.result;
    screen.src = "data:image/png;base64," + btoa(binary);
}

function getMousePos(screen, event){
    let rect = screen.getBoundingClientRect(),
        scaleX =  initWidth / screen.width,
        scaleY = initHeight / screen.height;
    console.log(`scales: ${scaleX} ${scaleY}`);
    return {
        x: (event.clientX - rect.left) * scaleX,
        y: (event.clientY - rect.top) * scaleY
    }
}

let reader = new FileReader();
reader.onload = screenUpdate;

let deboundHandler = debounce(moveHandler, 200);

function moveHandler(event){
    let pos = getMousePos(screen, event);

    console.log(`Sent ${pos.x} ${pos.y}`);
    socket.send(`move ${pos.x} ${pos.y}`);
}

function clickHandler(event){
    console.log("mouse " + event.button );
    socket.send("mouse " + event.button );
}


function keyHandler(event){
    let key = event.key;
    if (key == " "){
        key = "space";
    }
    console.log("key " + key);
    socket.send("key " + key)
}



function messageHandler(event){
    try {
        reader.readAsBinaryString(event.data);
    } catch (TypeError) {
        let data = event.data.split(" ");
        initWidth = data[1];
        initHeight = data[2];
        console.log(`Host resolution: ${initWidth}x${initHeight}`);        
    }
}

window.onload = function(){
    host = document.location.host;
    document.getElementById("h").innerText = `You are now controlling server located at: ${host}`

    screen = document.getElementById("screen");
    
    socket = new WebSocket("ws://" + host + "/ws");
    socket.onmessage = messageHandler;
    
    document.addEventListener('keydown', keyHandler);
}


