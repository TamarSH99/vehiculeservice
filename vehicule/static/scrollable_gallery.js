function get_images_list() {
    var images_list = []
    var filePath = "../static/vehicle_data/vehicle_data.json"
    fetch(filePath)
        .then(response => response.json())
        .then(data => {
            const result = JSON.stringify(data)
            parsed_result = JSON.parse(result)

            list_img = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]
            for (i = 0; i < 10; i++) {
                const myImage = document.getElementById(list_img[i]);
                const imageUrl = parsed_result[i]["image"]
                myImage.setAttribute("src", imageUrl);

            }

        })
        .catch(error => console.error(error));
}
get_images_list()

function get_properties_list(num) {
    if (num == 11)
        num = 1
    else
        if (num == 0)
            num = 10
    num = num - 1
    var filePath = "../static/vehicle_data/vehicle_data.json"
    fetch(filePath)
        .then(response => response.json())
        .then(data => {
            const result = JSON.stringify(data)
            parsed_result = JSON.parse(result)
            // Get a reference to the div element
            const showPropertiesDiv = document.getElementById('show_properties');

            // Get references to each p element inside the div car_number
            const car_number = document.getElementById('car_number');
            const modelP = document.getElementById('model');
            const time = document.getElementById('time');
            const kWhP = document.getElementById('kWh');
            const seatsP = document.getElementById('seats');
        
            // Set the text content of each p element
            car_number.textContent = String(num)
            modelP.textContent = String(parsed_result[num]["model"])
            time.textContent = String(parsed_result[num]["time"])
            kWhP.textContent = String(parsed_result[num]["kWh"])
            seatsP.textContent = String(parsed_result[num]["seats"])

        })
        .catch(error => console.error(error));
}

var currentIndex = 1;
displaySlides(currentIndex);

function setSlides(num) {
    displaySlides(currentIndex += num);
}
function displaySlides(num) {
    var slides = document.getElementsByClassName("imageSlides");
    if (num > 10) { currentIndex = 1 }
    if (num < 1) { currentIndex = 10 }
    for (var x = 0; x < 10; x++) {
        slides[x].style.display = "none";
    }
    console.log(num)
    get_properties_list(num)
    {
        slides[currentIndex - 1].style.display = "block";
    }

}

