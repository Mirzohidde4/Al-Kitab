document.addEventListener("click", function (event) {
    if (event.target.classList.contains("like-btn")) {
        let bookId = event.target.getAttribute("data-book-id");
        let likeButton = event.target;

        fetch(`/like/${bookId}/`, {
            method: "GET",
            headers: {
                "X-Requested-With": "XMLHttpRequest"
            },
            credentials: "same-origin"
        })
        .then(response => response.json())
        .then(data => {
            if (data.liked) {
                likeButton.innerHTML = "❤️ Liked";
                likeButton.setAttribute("data-liked", "true");
            } else {
                likeButton.innerHTML = "❤️";
                likeButton.setAttribute("data-liked", "false");
            }
        });
    }
});
