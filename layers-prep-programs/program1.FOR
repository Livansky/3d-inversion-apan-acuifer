      dimension zz(2000)
      character*12 arch
      logical lxmin, lx0, lxmax

      write (*,*) ' archivo de salida'
      read (*,'(bn,a)') arch
      open (unit=1, file=arch)

      write (*,*) ' numero de capa?'
      read (*,*) nc
      write (*,*) ' numero de prismas?'
      read (*,*) np
      write (*,*) ' cuanto vale xmin (10000=>variable)?'
      read (*,*) xmin
      if (xmin.eq.10000) then    
        lxmin=.true.
      else
        lxmin=.false.
      end if
      write (*,*) ' cuanto vale x0 (10000=>variable)?'
      read (*,*) x0
      if (x0.eq.10000) then    
        lx0=.true.
      else
        lx0=.false.
      end if
      write (*,*) ' cuanto vale xmax (10000=>variable)?'
      read (*,*) xmax
      if (xmax.eq.10000) then    
        lxmax=.true.
      else
        lxmax=.false.
      end if
      write (*,*) ' cuanto vale sx0?'
      read (*,*) sx0
      write (*,*) ' cuanto vale espesor minimo?'
      read (*,*) espmin
      write (*,*) ' cuanto vale el espesor maximo?'
      read (*,*) espmax
      if (lxmin.or.lx0.or.lxmax) then
        write (*,*) ' archivo con datos de batimetria?'
        read (*,'(bn,a)') arch
        open (unit=2, file=arch, status='old')
        do i=1, np
          read (2,*) dmy, zz(i)
        end do
        close (2)
      end if
      do i=1, np
        if (lxmin) xmin=zz(i)
        if (lx0) x0=zz(i)
        if (lxmax) xmax=zz(i)
        write (1,101) xmin, x0, xmax, sx0, espmin, espmax, nc, i
 101    format (6(1x,f9.3),2(1x,i5))
      end do
      close (1)
      stop ' o.k.'
      end

