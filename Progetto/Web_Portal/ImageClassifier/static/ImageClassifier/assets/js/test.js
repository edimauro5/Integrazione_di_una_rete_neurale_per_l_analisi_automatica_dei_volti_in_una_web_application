function readURL(input) {
    if (input.files && input.files[0]) {
        var reader = new FileReader();

        reader.onload = function (e) {
            document.getElementById('bannerImage').src = e.target.result;

        }
        reader.readAsDataURL(input.files[0]);
        document.getElementById('r_h_cont_id').style.removeProperty("border");
        document.getElementById('bannerImage').removeAttribute("hidden");
    }
}

function loading() {
    var elem = document.createElement("div");
    var i = 1;
    elem.setAttribute("id", "loader");
    elem.innerHTML = "<h3 id='frase' data-aos='zoom-in'>La rete neurale sta calcolando...</h3>";
    document.body.appendChild(elem);
    setInterval(function () {
        if (i == 1) {
            document.getElementById("loader").innerHTML = "<h3 id='frase' data-aos='zoom-in'>Aspetta ancora un po'...</h3>";
            i++;
        }
        else {
            document.getElementById("loader").innerHTML = "<h3 id='frase' data-aos='zoom-in'>La rete neurale sta calcolando...</h3>";
            i--;
        }
    }, 5000);
}

const allRanges = document.querySelectorAll(".range-wrap");
allRanges.forEach(wrap => {
    const range = wrap.querySelector(".form-range");
    const bubble = wrap.querySelector(".bubble");

    range.addEventListener("input", () => {
        setBubble(range, bubble);
    });
    setBubble(range, bubble);
});

function setBubble(range, bubble) {
    const val = range.value;
    const min = range.min ? range.min : 0;
    const max = range.max ? range.max : 1;
    const newVal = Number(((val - min) * 100) / (max - min));
    bubble.innerHTML = val;

    // Sorta magic numbers based on size of the native UI thumb
    bubble.style.left = `calc(${newVal}% + (${8 - newVal * 0.15}px))`;
}