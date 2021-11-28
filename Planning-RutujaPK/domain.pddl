(define (domain sokorobotto)
  (:requirements :typing)
  (:types
    shipment order location saleitem robot robot pallette - worker
  )
  (:predicates
    (ships ?s - shipment ?order - order)
    (available ?loc - location)
    (unstarted ?s - shipment)
    (packing-location ?loc - location)
    (contains ?p - pallette ?si - saleitem)
    (orders ?order - order ?si - saleitem)
    (connected ?loc - location ?p - location)
    (at ?w - worker ?loc - location)
    (no-robot ?loc - location)
    (no-pallette ?loc - location)
    (free ?robot - robot)
    (includes ?s - shipment ?si - saleitem)
    (cons ?s - shipment ?loc - location)
  )

  ;Function to Assign Location to a shipment
  (:action Ship_Availability
    :parameters (?shipment - shipment ?l - location)
    :precondition (and
      (unstarted ?shipment) ;the shipment hasn't started yet
      (packing-location ?l) ; We are looking for a packing location
      (available ?l) ;We are checking if the packing location is available
    )
    ; after the action is performed, following is the effect:
    :effect (and
      (not (unstarted ?shipment)) ;the unstarted shipment has started, therefore there is a not before the condition
      (not(available ?l)) ;Initially the location which was available for shipment is now not available as we have assigned that location to a shipment 
    )
  )

  ;Function to move the Robot 
  (:action Move_the_Robot
    :parameters (?robot - robot ?from - location ?to - location)
    :precondition (and
      (connected ?from ?to) ; check if the source and destination are connected
      (no-robot ?to) ;Check if the robot is already not present at the destination
      (at ?robot ?from) ; Check if the robot is present at the source location
    )
    ; after the action is performed, following is the effect:
    :effect (and
      (no-robot ?from) ;after the robot is moved from source the robot must not be present at source anymore.
      (at ?robot ?to) ;Check if the robot has successfully reached the destination
      (not (at ?robot ?from)) ;Check if the robot has successfully left the source 
      (not (no-robot ?to)) ;Initially there was no robot present at destination but after the action is performed the robot has reached the destination
    )
  )

  ;Function to move the robot and pallette
  (:action Move_Robot_And_Pallette
    :parameters (?robot - robot ?to - location ?from - location ?pallette - pallette)
    :precondition (and
      (connected ?from ?to) ; check if the source and destination are connected
      (free ?robot) ;Check if the robot is free to do the shipment 
      (no-robot ?to) ;Check if the robot is already not present at the destination
      (at ?robot ?from) ; Check if the robot is present at the source location
      (at ?pallette ?from) ; Check if the pallette is present at the source location
      (no-pallette ?to) ;Check if the pallette is already not present at the destination
    )
    ; after the action is performed, following is the effect:
    :effect (and
      (not (at ?robot ?from)) ;Check if the robot has successfully left the source 
      (no-robot ?from) ;after the robot is moved from source the robot must not be present at source anymore.
      (free ?robot) ;Check if the robot is free to do the shipment 
      (at ?robot ?to) ;Check if the robot has successfully reached the destination
      (not (at ?pallette ?from)) ;Check if the pallette has successfully left the source 
      (no-pallette ?from) ;after the pallette is moved from source the robot must not be present at source anymore.
      (not (no-pallette ?to)) ;Check if pallette has successfully reached destination
      (not (no-robot ?to)) ;Check if robot has successfully reached destination
      (at ?pallette ?to) ; Check if the pallette is present at the destination location

    )
  )

  ;Function to add items to the shipment at a shiping location if it is present in the order   
  (:action Add_Item_to_Order
    :parameters (?r - robot ?l - location ?p - pallette ?o - order ?si - saleitem ?s - shipment)
    :precondition (and
      (at ?p ?l) ;Check if the pallette is available at the location of pickup
      (free ?r) ; Check if the robot is free to carry forward the shipment
      (packing-location ?l) ;Check what the packing-location is
      (at ?r ?l) ;Check if the robot is at the packing-location
      (available ?l) ;Check if the packing-location is available to carry out shipment
      (not (no-pallette ?l)) ;Check if there are no pallette already ready to be shipped 
      (contains ?p ?si) ;Check if the pallette are there in the salesitem
      (orders ?o ?si) ;Check if the salesitems are a part of the order that is needed to be shipped 
      (ships ?s ?o) ;Checks and ships the order that contains the shipment that needs to be delivered
    )
    ; after the action is performed, following is the effect:
    :effect (and
      (not (contains ?p ?si)) ;Check if the salesitems do not contain the pallette anymore as they are going to be a part of the shipment 
      (includes ?s ?si) ; Check if the shipment that needs to be delivered contains all the required salesitems 
    )
  )
)