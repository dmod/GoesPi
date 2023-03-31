getAllImages = function (endpoint) {

  var xhr = new XMLHttpRequest();
  xhr.open('GET', endpoint, true);
  xhr.onload = function () {

    var imageRegex = /href="(.+\.jpg)"/g;
    var match;
    var imageList = [];
    while ((match = imageRegex.exec(xhr.responseText)) !== null) {
      imageList.push(endpoint + match[1]);
    }

    var dirRegex = /href="(.+\/)"/g;
    var match;
    var dirList = [];
    while ((match = dirRegex.exec(xhr.responseText)) !== null) {
      dirList.push(match[1]);
    }

    dirList = dirList.filter(image => image !== '../')

    dirList.forEach(x => getAllImages(endpoint + x));

    imageList.forEach(image => {

      console.log(image)

      var newHTMLImag = document.createElement('img');
      newHTMLImag.src = image
      newHTMLImag.width = 500
      newHTMLImag.height = 500

      document.getElementById('controls-and-images').appendChild(newHTMLImag);
    }

    )

  };
  xhr.send();

}

window.onload = function () {

  getAllImages('images/')

};