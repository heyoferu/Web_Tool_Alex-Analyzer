document.getElementById('file').addEventListener('change', function(e) {
    var file = e.target.files[0];
    if (file) {
        var reader = new FileReader();
        reader.onload = function(e) {
            document.getElementById('code').value = e.target.result;
        };
        reader.readAsText(file);
    }
});
