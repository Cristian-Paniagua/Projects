package main;

import java.util.Random;

import data_structures.ListQueue;
import interfaces.Queue;

public class PartMachine {

    private int id; 
    private CarPart p1;
    private int period;
    private double weightError;
    private int chanceOfDefective;
    private Queue<Integer> timer;
    private Queue<CarPart> conveyorBelt;
    private int totalPartsProduced;

   /**Constructor for PartMachine class
    * 
    * @param id
    * @param p1
    * @param period
    * @param weightError
    * @param chanceOfDefective
    */
    public PartMachine(int id, CarPart p1, int period, double weightError, int chanceOfDefective) {
        this.id = id;
        this.p1 = p1;
        this.period = period;
        this.weightError = weightError;
        this.chanceOfDefective = chanceOfDefective;
           
        this.timer = new ListQueue<Integer>();
        for(int i = this.period - 1; i >= 0; i--) {
            this.timer.enqueue(i);
        }
        
        this.conveyorBelt = new ListQueue<CarPart>();
        this.resetConveyorBelt();

        this.totalPartsProduced = 0;
        
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
    /**Timer getter
     * 
     * @return
     */
    public Queue<Integer> getTimer() {
        return timer;
    }
    /**Timer setter
     * 
     * @param timer
     */
    public void setTimer(Queue<Integer> timer) {
        this.timer = timer;
    }
    /**Part getter
     * 
     * @return
     */
    public CarPart getPart() {
       return p1;
    }
    /**Part setter
     * 
     * @param part1
     */
    public void setPart(CarPart part1) {
        this.p1 = part1;
    }
    /**ConveyorBelt getter
     * 
     * @return
     */
    public Queue<CarPart> getConveyorBelt() {
        return conveyorBelt;
    }
    /**ConveyorBelt setter
     * 
     * @param conveyorBelt
     */
    public void setConveyorBelt(Queue<CarPart> conveyorBelt) {
    	this.conveyorBelt = conveyorBelt;
    }
    /**TotalPartsProduced getter
     * 
     * @return
     */
    public int getTotalPartsProduced() {
         return totalPartsProduced;
    }
    /**TotalPartsProduced setter
     * 
     * @param count
     */
    public void setTotalPartsProduced(int count) {
    	this.totalPartsProduced = count;
    }
    /**WeightError getter
     * 
     * @return
     */
    public double getPartWeightError() {
        return weightError;
    }
    /**WeightError setter
     * 
     * @param partWeightError
     */
    public void setPartWeightError(double partWeightError) {
        this.weightError = partWeightError;
    }
    /**ChanceOfDefective getter
     * 
     * @return
     */
    public int getChanceOfDefective() {
        return chanceOfDefective;
    }
    /**ChanceOfDefective setter
     * 
     * @param chanceOfDefective
     */
    public void setChanceOfDefective(int chanceOfDefective) {
        this.chanceOfDefective = chanceOfDefective;
    }
    /**Method that clears the conveyorBelt and sets the size to 10
     * 
     */
    public void resetConveyorBelt() {
        conveyorBelt.clear();
        
        while(this.conveyorBelt.size() < 10) {
            this.conveyorBelt.enqueue(null);
        }
    }
    /**Method that returns the front of the timer and sets the front to last
     * 
     * @return
     */
    public int tickTimer() {
       int front = timer.front();
       timer.enqueue(timer.dequeue());
       return front;
    }
    /**Method that produces a CarPart and adds it to the conveyorBelt
     * 
     * @return
     */
    public CarPart produceCarPart() {	
    	
    	if(getPart() == null) {throw new NullPointerException();}

        Random rand = new Random();

        if(!getTimer().front().equals(0)) {
        	conveyorBelt.dequeue();
            conveyorBelt.enqueue(null);
        } else {

             double low = (double)(getPart().getWeight() - getPartWeightError());

             double high = (double)(getPart().getWeight() + getPartWeightError());

             double randomWeight =  low + (high - low) * rand.nextDouble(); 
            
            
            if(getTotalPartsProduced() % getChanceOfDefective() == 0 || getTotalPartsProduced() == 1) {
            	getPart().setDefective(true);
            } else {
            	getPart().setDefective(false);
            }

            CarPart newPart = new CarPart(getPart().getId(), getPart().getName(), randomWeight, getPart().isDefective());
            
            conveyorBelt.dequeue();
            conveyorBelt.enqueue(newPart);  
            
            this.totalPartsProduced++;
        }
            
            tickTimer();

       return this.getConveyorBelt().front();
    }

    /**
     * Returns string representation of a Part Machine in the following format:
     * Machine {id} Produced: {part name} {total parts produced}
     */
    @Override
    public String toString() {
        return "Machine " + this.getId() + " Produced: " + this.getPart().getName() + " " + this.getTotalPartsProduced();
    }
    /**
     * Prints the content of the conveyor belt. 
     * The machine is shown as |Machine {id}|.
     * If the is a part it is presented as |P| and an empty space as _.
     */
    public void printConveyorBelt() {
        // String we will print
        String str = "";
        // Iterate through the conveyor belt
        for(int i = 0; i < this.getConveyorBelt().size(); i++){
            // When the current position is empty
            if (this.getConveyorBelt().front() == null) {
                str = "_" + str;
            }
            // When there is a CarPart
            else {
                str = "|P|" + str;
            }
            // Rotate the values
            this.getConveyorBelt().enqueue(this.getConveyorBelt().dequeue());
        }
        System.out.println("|Machine " + this.getId() + "|" + str);
    }
}
