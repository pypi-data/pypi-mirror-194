from roulette_wheel import Wheel


def run( ) :
    # Get the degenerate gambler's name.
    name = input( 'Enter your name: ' )

    # Welcome them to the roulette model simulator.
    print( f'Welcome to the roulette wheel simulator, {name}' )

    # Create a model.
    roulette_wheel = Wheel( )

    # Run the model.
    result = roulette_wheel.random_spin( )
    print( result.color )
    print( result.number )

    # Exit
    print( "Have a good day!" )


# Press the green button in the gutter to run the script.
if __name__ == '__main__' :
    run( )

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
