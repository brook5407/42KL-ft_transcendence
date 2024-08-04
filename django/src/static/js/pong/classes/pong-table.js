class PongTable {
	constructor() {
		// calculate the width and height of the table from the window size
		this.width = window.innerWidth * 0.7;
		this.height = window.innerHeight * 0.7;
		this.table = document.createElement('canvas');
		this.table.width = this.width;
		this.table.height = this.height;
		this.context = this.table.getContext('2d');
	}
}
