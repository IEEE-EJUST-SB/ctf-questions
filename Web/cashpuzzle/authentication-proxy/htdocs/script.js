var selectedX = -1,
    selectedY = -1;
var numCorrect = 0;

function clickedOn(y, x) {
    console.log("Clicked on", y, x);

    if (selectedX == -1) {
        const img = document.getElementById(`${y}-${x}`);
        img.style = "border: 2px solid red;";

        selectedX = x;
        selectedY = y;
        return;
    }

    if (x == selectedX && y == selectedY) {
        console.log("Not swapping since element", y, x, "has been selected twice");
        const img = document.getElementById(`${y}-${x}`)
        img.style = "border: 2px solid transparent";
        selectedX = -1
        selectedY = -1
        return;
    }

    console.log("Swapping", y, x, "with", selectedY, selectedX);

    const imgElmId1 = `${selectedY}-${selectedX}`;
    const img1 = document.getElementById(imgElmId1);
    const imgId1 = imageIds[selectedY - 1][selectedX - 1];

    const imgElmId2 = `${y}-${x}`;
    const img2 = document.getElementById(imgElmId2);
    const imgId2 = imageIds[y - 1][x - 1];

    if (imgId1 == imgElmId1) numCorrect--;
    if (imgId2 == imgElmId2) numCorrect--;
    if (imgId1 == imgElmId2) numCorrect++;
    if (imgId2 == imgElmId1) numCorrect++;

    imageIds[selectedY - 1][selectedX - 1] = imgId2;
    imageIds[y - 1][x - 1] = imgId1;

    img1.style = "border: 2px solid transparent";

    const url1 = img1.src;
    const url2 = img2.src;

    img1.src = url2;
    img2.src = url1;

    selectedX = -1;
    selectedY = -1;

    loadFlagIfNecessary();
}

function loadImage(y, x) {
    const imageId = imageIds[y - 1][x - 1];
    const id = `${y}-${x}`;
    const url = `/proxy/puzzle/${imageId}.jpg`;
    const headers = {
        Authentication: "MD5",
    };

    fetch(url, { headers })
        .then((response) => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.blob();
        })
        .then((blob) => {
            const blobURL = URL.createObjectURL(blob);
            const img = document.getElementById(id);
            if (id == imageId) {
                numCorrect++;
                loadFlagIfNecessary();
            }
            img.src = blobURL;
        })
        .catch((error) => {
            console.log("Error: ", error);
        });
}

function loadFlagIfNecessary() {
    const flagElem = document.getElementById("flag");
    if (numCorrect == 16) {
        const headers = {
            Authorization: "MD5",
        };
        fetch("/proxy/puzzle/flag", { headers })
            .then((response) => {
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                return response.text();
            })
            .then((text) => {
                flagElem.innerText = text;
            })
            .catch((error) => {
                console.log("Error: ", error);
            });
    } else {
        flagElem.innerText = "";
    }
}

const array = Array.from({ length: 16 }, (_, idx) => {
    const i = Math.floor(idx / 4) + 1;
    const j = (idx % 4) + 1;
    return `${i}-${j}`;
});

// Shuffle the array
array.sort(() => Math.random() - 0.5);

imageIds = [
    array.slice(0, 4),
    array.slice(4, 8),
    array.slice(8, 12),
    array.slice(12, 16),
];

for (let y = 1; y <= 4; y++) {
    for (let x = 1; x <= 4; x++) {
        loadImage(y, x);
    }
}
