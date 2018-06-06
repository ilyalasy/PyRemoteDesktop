let HttpClient = function() {
    this.get = function(aUrl, aCallback) {
        let anHttpRequest = new XMLHttpRequest();
        anHttpRequest.responseType = "arraybuffer";
        anHttpRequest.onreadystatechange = function() { 
            if (anHttpRequest.readyState == 4 && anHttpRequest.status == 200)
                aCallback(anHttpRequest.response);
        }
        anHttpRequest.open( "GET", aUrl, true );            
        anHttpRequest.send( null );
    }
}

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

let client = new HttpClient();
let deboundHandler = debounce(moveHandler, 250)
let screen, initWidth, initHeight, host;



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

function moveHandler(event){
    let pos = getMousePos(screen, event);

    let rect = screen.getBoundingClientRect();
    console.log(`curr: ${event.clientX - rect.left} ${event.clientY - rect.top}`)
    
    client.get(`http://${host}/screenshot.png?x=${pos.x}&y=${pos.y}`, function(response){   
        getScreenshot();
    });
 
}

function clickHandler(event){
    client.get(`http://${host}/screenshot.png?click=true`, function(response){
        getScreenshot();
    });
}


function keyHandler(event){
    let key = event.key;
    if (key == " "){
        key = "space";
    }
    client.get(`http://${host}/screenshot.png?key=${key}`, function(response){
        getScreenshot();
    });
}

function setInitSizes(){
    let img = new Image();
    img.onload = function(){
        console.log(`sorce: ${img.width} ${img.height}`)
        console.log(`current: ${screen.width} ${screen.height}`)
        initWidth = img.width;
        initHeight = img.height;
    }
    img.src = "/screenshot.png";
}

function getScreenshot(){
    client.get(`http://${host}/screenshot.png`, function(response){
        var arrayBufferView = pako.deflate(new Uint8Array( response ));

        console.log("LENGTH:::");
        console.log(arrayBufferView.byteLength);
        var binary = '';
        for (let i = 0; i < arrayBufferView.byteLength; i++){
            binary += String.fromCharCode(arrayBufferView[i]);
        }
        screen.src = "data:image/png;base64," + btoa(binary);
    });

}

window.onload = function(){
    screen = document.getElementById("screen");

    host = document.location.host;
    document.getElementById("h").innerText = `You are now controlling server located at: ${host}`
    setInitSizes();
    document.addEventListener('keydown', keyHandler)

    getScreenshot();
}