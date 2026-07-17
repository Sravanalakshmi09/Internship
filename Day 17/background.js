const canvas = document.createElement("canvas");
document.body.prepend(canvas);

canvas.style.position = "fixed";
canvas.style.top = "0";
canvas.style.left = "0";
canvas.style.width = "100%";
canvas.style.height = "100%";
canvas.style.zIndex = "-10";
canvas.style.background = "#071421";

const ctx = canvas.getContext("2d");

let w, h;

function resize() {
    w = canvas.width = window.innerWidth;
    h = canvas.height = window.innerHeight;
}

resize();

window.addEventListener("resize", resize);

const mouse = {
    x: null,
    y: null
};

window.addEventListener("mousemove", e => {
    mouse.x = e.x;
    mouse.y = e.y;
});

class Particle {

    constructor() {

        this.x = Math.random() * w;
        this.y = Math.random() * h;

        this.vx = (Math.random() - 0.5) * 0.8;
        this.vy = (Math.random() - 0.5) * 0.8;

        this.radius = 2 + Math.random() * 2;

    }

    update() {

        this.x += this.vx;
        this.y += this.vy;

        if (this.x < 0 || this.x > w)
            this.vx *= -1;

        if (this.y < 0 || this.y > h)
            this.vy *= -1;

    }

    draw() {

        ctx.beginPath();

        ctx.arc(this.x, this.y, this.radius, 0, Math.PI * 2);

        ctx.fillStyle = "#00d9ff";

        ctx.fill();

    }

}

const particles = [];

for (let i = 0; i < 110; i++) {

    particles.push(new Particle());

}

function connect() {

    for (let a = 0; a < particles.length; a++) {

        for (let b = a; b < particles.length; b++) {

            let dx = particles[a].x - particles[b].x;

            let dy = particles[a].y - particles[b].y;

            let dist = Math.sqrt(dx * dx + dy * dy);

            if (dist < 150) {

                ctx.strokeStyle =
                    "rgba(0,217,255," + (1 - dist / 150) * 0.35 + ")";

                ctx.lineWidth = 1;

                ctx.beginPath();

                ctx.moveTo(
                    particles[a].x,
                    particles[a].y
                );

                ctx.lineTo(
                    particles[b].x,
                    particles[b].y
                );

                ctx.stroke();

            }

        }

    }

}

function mouseConnect() {

    if (mouse.x == null)
        return;

    particles.forEach(p => {

        let dx = p.x - mouse.x;

        let dy = p.y - mouse.y;

        let dist = Math.sqrt(dx * dx + dy * dy);

        if (dist < 180) {

            ctx.strokeStyle =
                "rgba(0,217,255," + (1 - dist / 180) * 0.8 + ")";

            ctx.beginPath();

            ctx.moveTo(p.x, p.y);

            ctx.lineTo(mouse.x, mouse.y);

            ctx.stroke();

        }

    });

}

function animate() {

    ctx.clearRect(0, 0, w, h);

    particles.forEach(p => {

        p.update();

        p.draw();

    });

    connect();

    mouseConnect();

    requestAnimationFrame(animate);

}

animate();