document.addEventListener("DOMContentLoaded", function () {
            let publishedDate = document.getElementById("published-date");
            publishedDate.addEventListener("mouseover", function () {
                let tooltip = this.getAttribute("title");
                this.setAttribute("data-original-title", tooltip);
                this.removeAttribute("title");
            });

            publishedDate.addEventListener("mouseleave", function () {
                let tooltip = this.getAttribute("data-original-title");
                this.setAttribute("title", tooltip);
            });
});
