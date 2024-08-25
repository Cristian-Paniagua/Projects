package main;

import java.time.LocalDate;
import java.time.temporal.ChronoUnit;

public class Book {

	private int id; 
	private String title;
	private String author;
	private String genre;
	private LocalDate lastCheckOut; 
	private boolean checkedOut;

	private LocalDate defaultCheckoutDate = LocalDate.of(2023, 9, 15);


	public Book(int id, String title, String author, String genre, LocalDate lastCheckOut, boolean checkedOut){
		this.id = id;
		this.title = title;
		this.author = author;
		this.genre = genre;
		this.lastCheckOut = lastCheckOut;
		this.checkedOut = checkedOut;
	}
	
	public int getId() {
		return this.id;
	}
	public void setId(int id) {
		this.id = id;
	}
	public String getTitle() {
		return this.title;
	}
	public void setTitle(String title) {
		this.title = title;
	}
	public String getAuthor() {
		return this.author;
	}
	public void setAuthor(String author) {
		this.author = author;
	}
	public String getGenre() {
		return this.genre;
	}
	public void setGenre(String genre) {
		this.genre = genre;
	}
	public LocalDate getLastCheckOut() {
		return this.lastCheckOut;
	}
	public void setLastCheckOut(LocalDate lastCheckOut) {
		this.lastCheckOut = lastCheckOut;
	}
	public boolean isCheckedOut() {
		return checkedOut;
	}
	public void setCheckedOut(boolean checkedOut) {
		this.checkedOut = checkedOut;
	}
	
	@Override
	public String toString() {
		/*
		 * This is supposed to follow the format
		 * 
		 * {TITLE} By {AUTHOR}
		 * 
		 * Both the title and author are in uppercase.
		 */

		return this.title.toUpperCase() + " BY " + this.author.toUpperCase();
	}
	public float calculateFees() {
		/*
		 * fee (if applicable) = base fee + 1.5 per additional day
		 */

		double baseFee = 10.00;
		double additionalFee = 1.50;
		float totalFee = 0;

		//this uses the ChronoUnit class to get the days that are between the given date and the date of the book since it was last checked out.
		double dayDifference = (double)ChronoUnit.DAYS.between(this.lastCheckOut, defaultCheckoutDate);

		if(dayDifference >= 31){
			totalFee = (float)(baseFee + additionalFee * (dayDifference - 31.00));
		}

		return totalFee;
	}
}
