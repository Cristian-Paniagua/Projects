package main;

import interfaces.Map;

public class Order {

    private int id;
    private String customerName;
    private Map<Integer, Integer> requestedParts;
    private boolean fulfilled;
   
    /**Constructor for Order class
     * 
     * @param id
     * @param customerName
     * @param requestedParts
     * @param fulfilled
     */
    public Order(int id, String customerName, Map<Integer, Integer> requestedParts, boolean fulfilled) {
        this.id = id;
        this.customerName = customerName;
        this.requestedParts = requestedParts;
        this.fulfilled = fulfilled;

    }
    /**Id getter
     * 
     * @return
     */
    public int getId() {
        return id;
    }
    /**Id setter
     * 
     * @param id
     */
    public void setId(int id) {
        this.id = id;
    }
    /**Fulfilled getter
     * 
     * @return
     */
    public boolean isFulfilled() {
      return fulfilled;
    }
    /**Fulfilled setter
     * 
     * @param fulfilled
     */
    public void setFulfilled(boolean fulfilled) {
        this.fulfilled = fulfilled;
    }
    /**RequestedParts getter
     * 
     * @return
     */
    public Map<Integer, Integer> getRequestedParts() {
       return requestedParts;
    }
    /**Requestedparts setter
     * 
     * @param requestedParts
     */
    public void setRequestedParts(Map<Integer, Integer> requestedParts) {
       this.requestedParts = requestedParts;
    }
    /**CustomerName getter
     * 
     * @return
     */
    public String getCustomerName() {
      return customerName;
    }
    /**CustomerName setter
     * 
     * @param customerName
     */
    public void setCustomerName(String customerName) {
        this.customerName = customerName;
    }
    /**
     * Returns the order's information in the following format: {id} {customer name} {number of parts requested} {isFulfilled}
     */
    @Override
    public String toString() {
        return String.format("%d %s %d %s", this.getId(), this.getCustomerName(), this.getRequestedParts().size(), (this.isFulfilled())? "FULFILLED": "PENDING");
    }

    
    
}
