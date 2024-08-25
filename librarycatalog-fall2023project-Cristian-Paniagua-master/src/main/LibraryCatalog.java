package main;

import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.File;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.time.LocalDate;
import java.util.stream.Collectors;

import data_structures.ArrayList;
import data_structures.DoublyLinkedList;
import data_structures.SinglyLinkedList;
import interfaces.FilterFunction;
import interfaces.List;

public class LibraryCatalog {

	private List<Book> bookCatalog;
	private List<User> users;

	private LocalDate defaultCheckoutDate = LocalDate.of(2023, 9, 15);

	public LibraryCatalog() throws IOException {

		bookCatalog = new SinglyLinkedList<Book>();
		users = new SinglyLinkedList<User>();

		bookCatalog = getBooksFromFiles();
		users = getUsersFromFiles();
	} 

	/**This method reads the catalog csv file and adds the books to a list.
	 * 
	 * @return
	 * @throws IOException
	 */
	private List<Book> getBooksFromFiles() throws IOException {

		List<Book> books = new SinglyLinkedList<Book>();
		
		try (BufferedReader reader = new BufferedReader(new FileReader("data/catalog.csv"))) {
		
			String line;
			int lineCount = 0; // adding a line count so it does not read the header line in the csv file.

			while((line = reader.readLine()) != null){
				String[] bookData = line.split(",");

				if(bookData.length == 6 && lineCount > 0){

					int id = Integer.parseInt(bookData[0].trim());
					String title = bookData[1].trim();
					String author = bookData[2].trim();
					String genre = bookData[3].trim();
					LocalDate lastCheckOut = LocalDate.parse(bookData[4].trim());
					boolean checkedOut = Boolean.parseBoolean(bookData[5].trim());

					books.add(new Book(id, title, author, genre, lastCheckOut, checkedOut)); // adds the book to the list
	
				}
				lineCount++;

			}
		}  
		
		return books;
	}
	
	/**This method reads the user csv file and adds the users to a list.
	 * 
	 * @return
	 * @throws IOException
	 */
	private List<User> getUsersFromFiles() throws IOException {

		List<User> users = new SinglyLinkedList<User>();

		try (BufferedReader reader = new BufferedReader(new FileReader("data/user.csv"))){

			String line;
			int lineCount = 0; // adding a line count so it does not read the header line in the csv file.

			

			while((line = reader.readLine()) != null) {
				String[] userData = line.split(",");
				List<Book> checkedOutBooks = new ArrayList<Book>();
				
				if(lineCount > 0){
					int id = Integer.parseInt(userData[0].trim());
					String name = userData[1].trim();

					if(userData.length == 3){

						String bookIdsStr = userData[2].trim();

						bookIdsStr = bookIdsStr.substring(1, bookIdsStr.length() - 1);

						String[] bookIds = bookIdsStr.split(" ");

						for (String bookId : bookIds) {
							int bookIdInt = Integer.parseInt(bookId.trim());
							Book book = findBookById(bookIdInt);
							if (book != null) {
								checkedOutBooks.add(book);
							}
						}
					}
					users.add(new User(id, name, checkedOutBooks)); // adds the User to the list
				}
				lineCount++;
			}	
		}	
		return users;
	}

	/** This a new private method that helps find the ids of the books.
	 * 
	 * @param bookId
	 * @return
	 */
	private Book findBookById(int bookId) { 
		for(Book book : bookCatalog) {
			if(book.getId() == bookId) {
				return book;
			}			
		}
		return null; // Returns null if the id was not found
	}
	public List<Book> getBookCatalog() {
		return bookCatalog;
	}
	public List<User> getUsers() {
		return users;
	}

	/** This methods adds a book to the catalog.
	 * 
	 * @param title the title of the book to be added
	 * @param author author of the book to be added
	 * @param genre genre of the book to be added
	 */
	public void addBook(String title, String author, String genre) {

		int newID = bookCatalog.size() + 1;

		bookCatalog.add(new Book(newID, title, author, genre, defaultCheckoutDate, false));

		return;
	}

	/**This method searched through the bookCatalog list for the book with the matching id and removes it.
	 * 
	 * @param id 
	 * @return 
	 */
	public void removeBook(int id) {

	// bookCatalog.remove(bookCatalog.firstIndex(bookCatalog.get(id)));

		for(Book book : bookCatalog){
			if(book.getId() == id){
				bookCatalog.remove(book);
			}
		}
		return;
	}	 


	/** This method searched through the bookCatalog list for the book with the matching id and if it is checked out.
	 * If it is not checked out, then changes status of checkedOut, else it updates the date.
	 * 
	 * @param id
	 * @return    
	 * 
	 */
	public boolean checkOutBook(int id) {

		boolean bookFound = false;
		for(Book book : bookCatalog){
			if(book.getId() == id && !book.isCheckedOut()){ //checks if the book matches the id and is checkedOut.
				book.setCheckedOut(true);
				return true;
			} else { 
				book.setLastCheckOut(defaultCheckoutDate); // changed the status of the checkout date.
			}
		}
		return bookFound;
	}

	/** This method searched through the bookCatalog list for the book with the matching id and if it is checkedOut.
	 * If if it checkedOut, then it return the book by changing the checkedOut status.
	 * 
	 * @param id
	 * @return
	 * 
	 */
	public boolean returnBook(int id) {

		for(Book book : bookCatalog){
			if(book.getId() == id && book.isCheckedOut()){
				book.setCheckedOut(false);
				return true;
			}
		}
		return false;
	}

	/** This method searched through the bookCatalog list for the book with the matching id and if it is CheckedOut.
	 * If it is checkeout out, it return true, meaning that it is available.
	 * 
	 * @param id
	 * @return 
	 * 
	 */
	public boolean getBookAvailability(int id) {

		for(Book book : bookCatalog){
			if(book.getId() == id && !book.isCheckedOut()){
				return true;
			}
		}
		return false;
	}

	/** This method the number of books with the same title and returns the amount.
	 * 
	 * @param title
	 * @return
	 * 
	 */
	public int bookCount(String title) {

		int count = 0;
		for(Book book : bookCatalog){
			if(book.getTitle().equals(title)){
				count++;
			}
		}
		return count;
	}

	/** This method returns the number of books with the same genre.
	 * 
	 * @param genre
	 * @return
	 */
	private int genreCount(String genre) {

		int count = 0;
		for(Book book : bookCatalog){
			if(book.getGenre().equals(genre)){
				count++;
			}
		}
		return count;
	}

	/** This method searched through the bookCatalog list for the books that are checkedOut and returns the total amount.
	 * 
	 * @return 
	 * 
	 */
	private int totalCheckedOutBooks(){

			int count = 0;
			for(Book book : bookCatalog){
				if(book.isCheckedOut()){
					count++;
				}
			}
				return count;
	}

	/** This method generates a report of the library.
	 * 
	 * @throws IOException
	 * @return 
	 * 
	 */
	public void generateReport() throws IOException {
		
		String output = "\t\t\t\tREPORT\n\n";
		output += "\t\tSUMMARY OF BOOKS\n";
		output += "GENRE\t\t\t\t\t\tAMOUNT\n";
		/*
		 * In this section you will print the amount of books per category.
		 * 
		 * Place in each parenthesis the specified count. 
		 * 
		 * Note this is NOT a fixed number, you have to calculate it because depending on the 
		 * input data we use the numbers will differ.
		 * 
		 * How you do the count is up to you. You can make a method, use the searchForBooks()
		 * function or just do the count right here.
		 */


		 
		output += "Adventure\t\t\t\t\t" + (genreCount("Adventure")) + "\n";
		output += "Fiction\t\t\t\t\t\t" + (genreCount("Fiction")) + "\n";
		output += "Classics\t\t\t\t\t" + (genreCount("Classics")) + "\n";
		output += "Mystery\t\t\t\t\t\t" + (genreCount("Mystery")) + "\n";
		output += "Science Fiction\t\t\t\t\t" + (genreCount("Science Fiction")) + "\n";
		output += "====================================================\n";
		output += "\t\t\tTOTAL AMOUNT OF BOOKS\t" + (bookCatalog.size()) + "\n\n";
		
		/*
		 * This part prints the books that are currently checked out
		 */
		output += "\t\t\tBOOKS CURRENTLY CHECKED OUT\n\n";
		/*
		 * Here you will print each individual book that is checked out.
		 * 
		 * Remember that the book has a toString() method. 
		 * Notice if it was implemented correctly it should print the books in the 
		 * expected format.
		 * 
		 * 
		 */

			for(Book book : bookCatalog){
				if(book.isCheckedOut()){
					output += book.toString() + "\n";
				}
			}

		output += "====================================================\n";
		output += "\t\t\tTOTAL AMOUNT OF BOOKS\t" + (totalCheckedOutBooks()) + "\n\n";

		/*
		 * Here we will print the users the owe money.
		 */
		output += "\n\n\t\tUSERS THAT OWE BOOK FEES\n\n";
		/*
		 * Here you will print all the users that owe money.
		 * The amount will be calculating taking into account 
		 * all the books that have late fees.
		 * 
		 * For example if user Jane Doe has 3 books and 2 of them have late fees.
		 * Say book 1 has $10 in fees and book 2 has $78 in fees.
		 * 
		 * You would print: Jane Doe\t\t\t\t\t$88.00
		 * 
		 * Notice that we place 5 tabs between the name and fee and 
		 * the fee should have 2 decimal places.
		 * 
		 * PLACE CODE HERE!
		 */
		
			
		float totalFeeOwed = 0;
			
		for(User user : users){
			float userFees = 0; 

			for(Book book : user.getCheckedOutList()){
				userFees += book.calculateFees();
			}

			totalFeeOwed += userFees;
			output += user.getName() + "\t\t\t\t\t" + "$" + userFees + "\n";
		}

			
		output += "====================================================\n";
		output += "\t\t\t\tTOTAL DUE\t$" + (totalFeeOwed) + "\n\n\n";
		output += "\n\n";
		System.out.println(output);// You can use this for testing to see if the report is as expected.
		
		/*
		 * Here we will write to the file.
		 * 
		 * The variable output has all the content we need to write to the report file.
		 * 
		 * 
		 */
		
		// this uses the BufferedWriter class to write the complete output of the report and printing it in the report file.
		try(BufferedWriter writer = new BufferedWriter(new FileWriter("report/expected_report.txt"))){ 
				writer.write(output, 0, output.length());
		}
	}
	
	/*
	 * BONUS Methods
	 * 
	 * You are not required to implement these, but they can be useful for
	 * other parts of the project.
	 */
	public List<Book> searchForBook(FilterFunction<Book> func) {
		return null;
	}
	
	public List<User> searchForUsers(FilterFunction<User> func) {
		return null;
	}
	
}
