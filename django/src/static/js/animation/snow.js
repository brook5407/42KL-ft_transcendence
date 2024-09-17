export class Snowfall {
    constructor() {
        this.snowflakes = [];
        this.snowflakeImageSrc = '/static/images/snowflake.svg';
        this.updateInterval = null;
        this.updateSnowflakeCount();
    }

    updateSnowflakeCount() {
        const count = this.getCookie('snow_intensity');
        this.snowflakeCount = count ? Number(count) : 50;
    }

    getCookie(name) {
        const value = `; ${document.cookie}`;
        const parts = value.split(`; ${name}=`);
        if (parts.length === 2) return parts.pop().split(';').shift();
    }

    async createSnowflakes() {
        const createOneSnowflake = () => {
            const snowflake = new Image();
            snowflake.src = this.snowflakeImageSrc;
            snowflake.alt = 'Snowflake';
            snowflake.classList.add('blur', 'snowflake');
            snowflake.style.left = Math.random() * 100 + 'vw';
            snowflake.style.animationDelay = '0s';
            snowflake.style.animationDuration = Math.random() * 3 + 2 + 's';
            snowflake.style.animationTimingFunction = 'linear';
            snowflake.style.width = snowflake.style.height =
                Math.random() * 30 + 10 + 'px';
            snowflake.style.opacity = Math.random();
            snowflake.style.zIndex = -1;

            document.body.appendChild(snowflake);
            this.snowflakes.push(snowflake);

            const spinAnimation =
                Math.random() > 0.5 ? 'spin-clockwise' : 'spin-anticlockwise';
            snowflake.style.animationName = `fall, ${spinAnimation}`;

            snowflake.addEventListener('animationend', () => {
                this.resetSnowflake(snowflake);
            });
        };

        while (this.snowflakes.length < this.snowflakeCount) {
            await this.sleep(Math.random() * 100);
            createOneSnowflake();
        }

        // Remove excess snowflakes if the count has decreased
        while (this.snowflakes.length > this.snowflakeCount) {
            const snowflake = this.snowflakes.pop();
            snowflake.remove();
        }
    }

    resetSnowflake(snowflake) {
        snowflake.style.left = Math.random() * 100 + 'vw';
        snowflake.style.animationDuration = Math.random() * 3 + 2 + 's';
        snowflake.style.animationName = 'none';
        void snowflake.offsetWidth;
        const spinAnimation =
            Math.random() > 0.5 ? 'spin-clockwise' : 'spin-anticlockwise';
        snowflake.style.animationName = `fall, ${spinAnimation}`;
    }

    startSnowfall() {
        this.createSnowflakes();
        this.startUpdateCheck();
    }

    stopSnowfall() {
        this.snowflakes.forEach((snowflake) => {
            snowflake.remove();
        });
        this.snowflakes = [];
        this.stopUpdateCheck();
    }

    startUpdateCheck() {
        this.updateInterval = setInterval(() => {
            const oldCount = this.snowflakeCount;
            this.updateSnowflakeCount();
            if (oldCount !== this.snowflakeCount) {
                this.createSnowflakes();
            }
        }, 5000); // Check every 5 seconds
    }

    stopUpdateCheck() {
        if (this.updateInterval) {
            clearInterval(this.updateInterval);
            this.updateInterval = null;
        }
    }

    sleep(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }
}