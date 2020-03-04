import { Component, OnInit, Output, Input, EventEmitter } from '@angular/core';
import { Subscription } from 'rxjs';

import { ConnectService } from '../connect.service'

import * as d3 from "d3";

@Component({
  selector: 'app-d3-graph',
  templateUrl: './d3-graph.component.html',
  styleUrls: ['./d3-graph.component.scss']
})
export class D3GraphComponent implements OnInit {

 @Output()
 onClose: EventEmitter<boolean> = new EventEmitter();

 graphDataSubscription: Subscription;

graphData;

@Input()
IDgraph: string;

  constructor(private data: ConnectService) {}

  ngOnInit(): void {

    this.graphDataSubscription = this.data.graphDataSubject.subscribe((graphData: any[]) => 
		{
      this.graphData = graphData;

      this.createGraph();
		}
		)
		
	this.data.getGraphData(this.IDgraph); 



  }

  createGraph()
  {

    console.log(this.graphData);
    
  const links = this.graphData.links.map(d => Object.create(d));
  const nodes = this.graphData.nodes.map(d => Object.create(d));

 
  var width = 600;
  var height = 600;

  const simulation = d3.forceSimulation(nodes)
      .force("link", d3.forceLink(links).id(d => d.id))
	//.force("charge", d3.forceManyBody())
	.force("collide", d3.forceCollide().radius((d) => {
    return 70;
  }))
	.force("center", d3.forceCenter(width /2 , height/2-30))
	  
	var svg = d3.select("#theSVG")
	.attr("viewBox", [0, 0, width, height]);

  const link = svg.append("g")
      .attr("stroke", "#999")
      .attr("stroke-opacity", 0.6)
    .selectAll("line")
    .data(links)
    .join("line");
      
  const node = svg.append("g")
      
    .selectAll("g")	
    .data(nodes)

    .join("g");
	
	
	const nodeA = node.filter((d) => {
		return typeof(d.Nature) == "undefined";
		
	});
	
	nodeA.append("rect")	
      .attr("height", 50)
	  .attr("width", 100)
      .attr("fill", "rgb(208,74,2)");
	  
	  nodeA.append("rect")
	  .attr("height",5)
	  .attr("width", 100)
	  .attr("y", 50)
	  .attr("fill", "rgb(235,140,0)");

	  
    var text = nodeA.append("text")
	  .text(d => d.id)
	  .attr("x", 0)
      .attr("y", 15)
	  .attr("dy", 0)
	  .attr("font-family","arial")
	  .attr("fill", "white")
	 ;
	  
	  this.wrap(text, 50);
	  
	  
	 const nodeB = node.filter((d) => {
		return typeof(d.Nature) != "undefined";
		
	});
	  
	 nodeB.append("image").attr("href", "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAQAAAAEACAMAAABrrFhUAAAAM1BMVEX///+vvcOPo63W3eC8yM7N19vr7e8otfUCmeP9/f0otfUCmePr7e/N19uOoqx4j5tUbnpjZSvSAAAADnRSTlP//////////////v7+/r+gP8AAAAMwSURBVHgB7dzx7tIwFMXxim5wtlV8/6d1d5CYjvwkTthlOd+DJMJ/+3h319LW8izf3pzTm1M2BwAAAAAAAAAA+H5sgB/l0wWSrz9fIPn68wWSrz9fIPn68wWSrz9fIPn68wUOcf2R7mApLwsAAAAAAAAAANC/KccBAAAAAAAAAAAAzqv87/eXe7p7Lm22fA8AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABI1hslJe+dolpzSF4ArYDcK0D2PcDuFohI1hVgfwu0FRAxGwhJ3iNBrTlkBvA4DpBbBZgDFMkcoCWQxO8B3hVQ5AVAD+ApIPOBkOyboFoC93EAkyEZVkDD4QYAgCJFznMBHoMqznMBxdt4KAxAW/Q0QZqgZN8DijMAABHnHsA2OZlOhsynwwBY/ypME/wT8Ri0/FVYHzASBGAYhnHMAlDzMQVgWCpgzB8JKmmr7NRPU+1qymZpxZ82KQB9lwEQ0crDrAJaAJUsgL7v8m+BLIAQmCug5u8WDw9Z7RZXJLEJRvNbGsD8rrV293fd+ciM0iogrv2m0E/RA26v1+QQK0MBMAzLOGiIgVCMBuuctMlQAkDfAMyvLkohdSQo7QpwngECYRwXgNwKYDqsIu0LMMU/f+Q2GRpzAeJz2Rkg/p4LoJILEA1gTjwD4l1zp8NF2r0ChuU1Xm6vmrEw0iShB9wBxgSA9XSQlSEAZL46rGK9VZb9Ad5LY6wMARCxA2B/AI9B8+PzBQBnAEmcF+C8AIemODTFoSmaIE3QdKusHhs/AObTYTk3QcmwAtqIx6D7gQnvuUBE3gBScZ4LSOb/s3TEDUDyroDHHmANEJE5gBx7gGMFNLHuAZE9ZoMvANhhaSxiCGBdAZLUfra/BWQOIMdbwL0CHHtAwq/Cp7/n5/VJDrk2CAAAAAAAAAAANPn1j+maHBkAAAAAAAAAAAC4fhEAAAAAAAAAAAAAAAAAAAAAAADgkwG2ZzvA9gDwPAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAHDaOdedUwAAAAAAAAAAAAAAAAAAAAAAAIDfn1fFYmSQMdAAAAAASUVORK5CYII=").attr("height", 50);
	  

	  
	  simulation.on("tick", () => {
		  
		
		  var k = 0.01;
		  var l = 1;
		  
    link.attr("x1", d => d.source.x)
        .attr("y1", d => d.source.y)
        .attr("x2", d => d.target.x)
        .attr("y2", d => d.target.y);

        node.attr("transform", d => `translate(${d.x-50},${d.y-25})`).each(d  => 
			{
				d.y = d.__proto__.layer*height/d.__proto__.total_layer;
				
			});
			
		;
		
  }) ;
  }

 wrap(text, width) {
  text.each(function() {
    var text = d3.select(this),
        words = text.text().split(/\s+/).reverse(),
        word,
        line = [],
        lineNumber = 0,
        lineHeight = 1.1, // ems
        y = text.attr("y"),
        dy = parseFloat(text.attr("dy")),
        tspan = text.text(null).attr("font-size", "12px").attr("x", 3).attr("y", y).attr("dy", dy + "em");
    while (word = words.pop()) {
      line.push(word);
      tspan.text(line.join(" "));
      if (tspan.node().getComputedTextLength()*.5 > width) {
        line.pop();
        tspan.text(line.join(" "));
        line = [word];
        tspan = text.append("tspan").attr("x", 3).attr("y", y).attr("dy", ++lineNumber * lineHeight + dy + "em").text(word);
      }
    }
  });
}

  hideMe()
  {
   this.onClose.emit(); 
  }


}
