      character*12 arch

      dimension iraro(3000)

      write (*,*) ' archivo de entrada?'

      read (*,'(bn,a)') arch

      open (unit=1, file=arch,status='old')

      write (*,*) ' archivo de entrada con prismas aflorantes?'

      read (*,'(bn,a)') arch

      open (unit=2, file=arch,status='old')

      do i=1, 3000

        read (2,*, end=10) iraro(i)

      end do

10    continue

      nraro = i-1

      write (*,*) ' archivo de salida'

      read (*,'(bn,a)') arch

      open (unit=3, file=arch)

      write (*,*) 'dame xmin- x0 y xmax..(10000=>no cambio)'

      read (*,*) xrmin, xr0,xrmax

      write (*,*) 'dame sx- espmin- espmax(10000=>no cambio)'

      read (*,*) srx, ermin, ermax
      write (*,*) ' dmae shifting para xmin (puede ser 0), x0 y xmax'
      read (*,*) xshift, xshift2, xshift3

      do i=1, 1000000

         read (1,*,end=20) x1,x2,x3, x4,x5,x6, nc, np

         do j=1, nraro

           if (np.eq.iraro(j)) then

               if (xrmin.ne.10000) then
			   x1 = xrmin
               else 
                 x1 = x1+xshift
               end if

c               if (xr0.ne.10000) x2 = xr0
c
c               if (xrmax.ne.10000) x3 = xrmax
               if (xr0.ne.10000) then
                  x2 = xr0
               else
                  x2 = x2+xshift2
               end if

               if (xrmax.ne.10000) then
                  x3 = xrmax
               else
                  x3 = x3+xshift3
               end if

               if (srx.ne.10000)  x4 = srx

               if (ermin.ne.10000) x5 = ermin

               if (ermax.ne.10000) x6 = ermax

           end if

         end do

         write (3,101) x1, x2, x3, x4, x5, x6, nc, np

 101     format (6(1x,f9.3),2(1x,i5))

      end do

 20   continue

      close (1)

      close (2)

      close (3)

      stop ' o.k.'

      end



