window.onload = function () {
  // Get the slider container and trackbar elements
  var sliderContainer = document.getElementById("slider-container");
  var sliderTrackbar = document.getElementById("slider-trackbar");

  // Get the directory listing and extract the image URLs
  var xhr = new XMLHttpRequest();
  xhr.open('GET', 'images/goes16/fd/fc/2023-03-31/', true);
  xhr.onload = function () {
    // Extract the image URLs from the directory listing
    var regex = /href="(.+\.jpg)"/g;
    var match;
    var imageList = [];
    while ((match = regex.exec(xhr.responseText)) !== null) {
      imageList.push('images/goes16/fd/fc/2023-03-31/' + match[1]);
    }

    // Preload and add the images to the slider container
    for (var i = 0; i < imageList.length; i++) {
      var container = document.createElement("div");
      container.classList.add("slider-image-container");

      var img = new Image();
      img.src = imageList[i];

      img.onload = (function (container, img, filename) {
        return function () {
          container.appendChild(img);

          //var text = document.createElement("div");
          //text.classList.add("slider-image-text");
          //text.innerText = filename;
          //container.appendChild(text);

          sliderContainer.appendChild(container);
          sliderTrackbar.max = imageList.length - 1;

          sliderTrackbar.value = 0
          sliderTrackbar.dispatchEvent(new Event("input"))

        }
      })(container, img, imageList[i].split('/').pop());
    }

  };
  xhr.send();

  // Add event listener for the trackbar to update the active image
  sliderTrackbar.addEventListener("input", function () {
    var activeImage = sliderContainer.querySelector("img.active");
    if (activeImage) {
      activeImage.classList.remove("active");
    }
    var newActiveImage = sliderContainer.querySelectorAll("img")[this.value];
    newActiveImage.classList.add("active");
  });
};