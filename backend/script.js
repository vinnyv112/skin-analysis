
function goDetail(title) {
    window.location.href = "detail.html?title=" + title;
}

function previewImage(event) {
    document.getElementById("preview").src =
        URL.createObjectURL(event.target.files[0]);
}

function showResult() {
    document.getElementById("result").style.display = "block";
}
function goDetail(type) {
    if (type === 'Oily Skin') {
        window.location.href = 'oily.html';
    } else if (type === 'Sensitive Skin') {
        window.location.href = 'sensitive.html';
    } else if (type === 'Dry Skin') {
        window.location.href = 'dry.html';
    } else if (type === 'Acne-Prone Skin') {
        window.location.href = 'acne.html';
    } else if (type === 'Cleanser') {
        window.location.href = 'cleanser.html';
    } else if (type === 'Moisturizer') {
        window.location.href = 'moisturizer.html';
    } else if (type === 'Serum') {
        window.location.href = 'serum.html';
    } else if (type === 'Sunscreen') {
        window.location.href = 'sunscreen.html';
    }else if (type === 'Vitamin C') {
        window.location.href = 'Vitaminc.html';
    }else if (type === 'AHA / BHA') {
        window.location.href = 'aha.html';
    }else if (type === 'Salicylic Acid') {
        window.location.href = 'Salicylic.html';
    }else if (type === 'Niacinamide') {
        window.location.href = 'Niacinamide.html';
    }
}