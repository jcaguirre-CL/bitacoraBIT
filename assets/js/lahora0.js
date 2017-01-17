			function updateClock() {
    			var now = new Date(), // current date
        			months = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo','Junio', 'Julio', 'Agosto','Septiembre', 'Octubre', 'Noviembre', 'Diciembre']; // you get the idea
        			time = now.getHours() + ':' + now.getMinutes() + ':' + now.getSeconds(), // again, you get the idea

        			// a cleaner way than string concatenation
        			date = [now.getDate(),
        					months[now.getMonth()],
        					now.getFullYear()].join(' ');

        			// set the content of the element with the ID time to the formatted string
        			document.getElementById('fecha').innerHTML = [date, time].join(' / ');
        			// call this function again in 1000ms
        			setTimeout(updateClock, 1000);
			}
            updateClock(); // initial call
